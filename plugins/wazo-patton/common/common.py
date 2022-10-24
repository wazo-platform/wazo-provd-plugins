# Copyright 2016-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import os.path
import re

from operator import itemgetter
from provd import synchronize, tzinform
from provd.plugins import (
    FetchfwPluginHelper,
    StandardPlugin,
    TemplatePluginHelper,
)
from provd.devices.pgasso import (
    BasePgAssociator,
    COMPLETE_SUPPORT,
    FULL_SUPPORT,
    IMPROBABLE_SUPPORT,
    UNKNOWN_SUPPORT,
)
from provd.servers.http import HTTPNoListingFileService
from provd.util import format_mac, norm_mac
from twisted.internet import defer, threads

logger = logging.getLogger('plugin.wazo-patton')


class BasePattonHTTPDeviceInfoExtractor:

    _UA_REGEX = re.compile(r'^SmartNode \(Model:(\w+)/[^;]+; Serial:(\w+); Software Version:R([^ ]+)')

    def extract(self, request, request_type):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request):
        ua = request.getHeader('User-Agent')
        if ua:
            return self._extract_from_ua(ua)
        return None

    def _extract_from_ua(self, ua):
        # HTTP User-Agent:
        #   "SmartNode (Model:SN4112/JS/EUI; Serial:00A0BA08933C; Software Version:R6.2 2012-09-11 H323 SIP FXS FXO; Hardware Version:4.4)"
        #   "SmartNode (Model:SN4316/JS; Serial:00A0BA0BA9A5; Software Version:R6.9 2016-07-05 H323 SIP FXS FXO; Hardware Version:2.3)"
        m = self._UA_REGEX.match(ua)
        if m:
            raw_model, raw_mac, raw_version = m.groups()
            try:
                mac = norm_mac(raw_mac.decode('ascii'))
            except ValueError as e:
                logger.warning('Could not normalize MAC address: %s', e)
            else:
                return {'vendor': 'Patton',
                        'model': raw_model.decode('ascii'),
                        'version': raw_version.decode('ascii'),
                        'mac': mac}


class BasePattonPgAssociator(BasePgAssociator):

    def __init__(self, models, version):
        self._models = models
        self._version = version

    def _do_associate(self, vendor, model, version):
        if vendor == 'Patton':
            if model in self._models:
                if version == self._version:
                    return FULL_SUPPORT
                return COMPLETE_SUPPORT
            return UNKNOWN_SUPPORT
        return IMPROBABLE_SUPPORT


class _TimezoneConverter:

    _DAYS_DEFAULT_SUFFIX = 'th'
    _DAYS_SUFFIX = {
        1: 'st',
        2: 'nd',
        3: 'rd',
        11: 'st',
        12: 'nd',
        13: 'rd',
        21: 'st',
        22: 'nd',
        23: 'rd',
        31: 'st',
    }
    _DAYS_OF_WEEK = [
        'monday',
        'tuesday',
        'wednesday',
        'thursday',
        'friday',
        'saturday',
        'sunday',
    ]
    _MONTHS = [
        'jan',
        'feb',
        'mar',
        'apr',
        'may',
        'jun',
        'jul',
        'aug',
        'sep',
        'oct',
        'nov',
        'dec',
    ]
    _WEEKS = [
        'first',
        'second',
        'third',
        'fourth',
        'last',
    ]

    def __init__(self, tzinfo):
        self._tzinfo = tzinfo

    def default_offset(self):
        return self._format_time_as_offset(self._tzinfo['utcoffset'])

    def has_dst(self):
        return self._tzinfo['dst'] is not None

    def dst_offset(self):
        tz_time = tzinform.Time(self._tzinfo['utcoffset'].as_seconds + self._tzinfo['dst']['save'].as_seconds)
        return self._format_time_as_offset(tz_time)

    def dst_start(self):
        return self._format_dst_change(self._tzinfo['dst']['start'])

    def dst_end(self):
        return self._format_dst_change(self._tzinfo['dst']['end'])

    def _format_time(self, tz_time):
        hours, minutes, _ = tz_time.as_hms
        return f'{hours:02d}:{minutes:02d}'

    def _format_time_as_offset(self, tz_time):
        hours, minutes, _ = tz_time.as_hms
        if hours < 0 or minutes < 0:
            sign = '-'
        else:
            sign = '+'
        return f'{sign}{abs(hours):02d}:{abs(minutes):02d}'

    def _format_dst_change(self, dst_change):
        fmted_time = self._format_time(dst_change['time'])
        fmted_month = self._convert_month(dst_change['month'])
        day = dst_change['day']
        if day.startswith('D'):
            day = int(day[1:])
            day_rule = self._convert_day(day)
        else:
            week, day_of_week = int(day[1]), int(day[3])
            fmted_day_of_week = self._convert_day_of_week(day_of_week)
            fmted_week = self._convert_week(week)
            day_rule = f'{fmted_week} {fmted_day_of_week}'
        return f'{fmted_time} {fmted_month} {day_rule}'

    def _convert_day(self, day):
        suffix = self._DAYS_SUFFIX.get(day, self._DAYS_DEFAULT_SUFFIX)
        return f'{day:d}{suffix}'

    def _convert_day_of_week(self, day_of_week):
        return self._DAYS_OF_WEEK[tzinform.week_start_on_monday(day_of_week) - 1]

    def _convert_month(self, month):
        return self._MONTHS[month - 1]

    def _convert_week(self, week):
        return self._WEEKS[week - 1]


class _SIPLinesConverter:

    def __init__(self):
        self._lines = []
        self._servers = []
        self._next_server_id = 1

    def add_sip_line(self, sip_line_no, sip_line):
        line = self._build_line(sip_line_no, sip_line)
        server = self._build_server(sip_line, 'proxy_ip', 'proxy_port')
        if 'backup_proxy_ip' in sip_line:
            backup_server = self._build_server(sip_line, 'backup_proxy_ip', 'backup_proxy_port')
        else:
            backup_server = None

        line['servers'].append(server)
        server['lines'].append(line)
        if backup_server is not None:
            line['servers'].append(backup_server)
            backup_server['lines'].append(line)

    def _build_line(self, sip_line_no, sip_line):
        line_no = int(sip_line_no)
        username = sip_line['username']
        for existing_line in self._lines:
            if existing_line['username'] == username:
                raise Exception(
                    f'username {username} is referenced by both lines {line_no} and {existing_line["line_no"]}'
                )
        line = self._new_line(line_no, sip_line)
        self._lines.append(line)
        return line

    def _new_line(self, line_no, sip_line):
        line = {
            'line_no': line_no,
            'fxs_port_no': line_no - 1,
            'auth_username': sip_line['auth_username'],
            'username': sip_line['username'],
            'password': sip_line['password'],
            'proxy_ip': sip_line['proxy_ip'],
            'registrar_ip': sip_line.get('registrar_ip', sip_line['proxy_ip']),
            'registrar_port': sip_line.get('registrar_port', '5060'),
            'servers': [],
        }
        if 'backup_proxy_ip' in sip_line:
            line['backup_registrar_ip'] = sip_line.get('backup_registrar_ip', sip_line['backup_proxy_ip'])
            line['backup_registrar_port'] = sip_line.get('backup_registrar_port', '5060')
        return line

    def _build_server(self, sip_line, key_proxy_ip, key_proxy_port):
        proxy_ip = sip_line[key_proxy_ip]
        proxy_port = sip_line.get(key_proxy_port, '5060')
        for existing_server in self._servers:
            if existing_server['proxy_ip'] == proxy_ip:
                if existing_server['proxy_port'] != proxy_port:
                    raise Exception(
                        f'proxy {proxy_ip} is referenced with both port {proxy_port} '
                        f'and {existing_server["proxy_port"]}'
                    )
                return existing_server
        server = self._new_server(proxy_ip, proxy_port)
        self._servers.append(server)
        return server

    def _new_server(self, proxy_ip, proxy_port):
        server = {
            'id': self._next_server_id,
            'proxy_ip': proxy_ip,
            'proxy_port': proxy_port,
            'lines': [],
        }
        self._next_server_id += 1
        return server

    def lines(self):
        return sorted(self._lines, key=itemgetter('line_no'))

    def servers(self):
        return list(self._servers)


class BasePattonPlugin(StandardPlugin):

    _ENCODING = 'ascii'
    _SIP_DTMF_MODE = {
        'RTP-in-band': 'default',
        'RTP-out-of-band': 'rtp',
        'SIP-INFO': 'signaling'
    }

    def __init__(self, app, plugin_dir, gen_cfg, spec_cfg):
        StandardPlugin.__init__(self, app, plugin_dir, gen_cfg, spec_cfg)

        self._tpl_helper = TemplatePluginHelper(plugin_dir)

        downloaders = FetchfwPluginHelper.new_downloaders(gen_cfg.get('proxies'))
        fetchfw_helper = FetchfwPluginHelper(plugin_dir, downloaders)

        self.services = fetchfw_helper.services()
        self.http_service = HTTPNoListingFileService(self._tftpboot_dir)

    http_dev_info_extractor = BasePattonHTTPDeviceInfoExtractor()

    def _add_syslog_level(self, raw_config):
        if 'syslog_level' in raw_config:
            if raw_config['syslog_level'] == 'info':
                raw_config['XX_syslog_level'] = 'informational'
            else:
                raw_config['XX_syslog_level'] = raw_config['syslog_level']

    def _add_timezone_and_dst(self, raw_config):
        if 'timezone' in raw_config:
            try:
                tzinfo = tzinform.get_timezone_info(raw_config['timezone'])
            except tzinform.TimezoneNotFoundError as e:
                logger.info('Unknown timezone: %s', e)
            else:
                converter = _TimezoneConverter(tzinfo)
                raw_config['XX_timezone_offset'] = converter.default_offset()
                if converter.has_dst():
                    raw_config['XX_dst_offset'] = converter.dst_offset()
                    raw_config['XX_dst_start'] = converter.dst_start()
                    raw_config['XX_dst_end'] = converter.dst_end()

    def _update_sip_transport(self, raw_config):
        if 'sip_transport' not in raw_config:
            raw_config['sip_transport'] = 'udp'
        elif raw_config.get('sip_transport') == 'tls':
            logger.warning("Patton doesn't support the SIP transport tls: fallback to udp")
            raw_config['sip_transport'] = 'udp'

    def _add_dtmf_relay(self, raw_config):
        if 'sip_dtmf_mode' in raw_config:
            raw_config['XX_dtmf_relay'] = self._SIP_DTMF_MODE[raw_config['sip_dtmf_mode']]

    def _add_lines_and_servers(self, raw_config):
        converter = _SIPLinesConverter()
        for sip_line_no, sip_line in raw_config['sip_lines'].items():
            converter.add_sip_line(sip_line_no, sip_line)
        raw_config['XX_lines'] = converter.lines()
        raw_config['XX_servers'] = converter.servers()

    _SENSITIVE_FILENAME_REGEX = re.compile(r'^[0-9a-f]{12}\.cfg$')

    def _dev_specific_filename(self, device):
        fmted_mac = format_mac(device['mac'], separator='')
        return fmted_mac + '.cfg'

    def _check_device(self, device):
        if 'mac' not in device:
            raise Exception('MAC address needed for device configuration')

    def configure(self, device, raw_config):
        self._check_device(device)
        filename = self._dev_specific_filename(device)
        tpl = self._tpl_helper.get_dev_template(filename, device)

        self._add_syslog_level(raw_config)
        self._add_timezone_and_dst(raw_config)
        self._update_sip_transport(raw_config)
        self._add_dtmf_relay(raw_config)
        self._add_lines_and_servers(raw_config)

        path = os.path.join(self._tftpboot_dir, filename)
        self._tpl_helper.dump(tpl, raw_config, path, self._ENCODING, errors='ignore')

    def deconfigure(self, device):
        path = os.path.join(self._tftpboot_dir, self._dev_specific_filename(device))
        try:
            os.remove(path)
        except OSError as e:
            logger.info('error while removing file: %s', e)

    if hasattr(synchronize, 'standard_sip_synchronize'):
        def synchronize(self, device, raw_config):
            return synchronize.standard_sip_synchronize(device)

    else:
        # backward compatibility with older wazo-provd server
        def synchronize(self, device, raw_config):
            try:
                ip = device['ip'].encode('ascii')
            except KeyError:
                return defer.fail(Exception('IP address needed for device synchronization'))
            else:
                sync_service = synchronize.get_sync_service()
                if sync_service is None or sync_service.TYPE != 'AsteriskAMI':
                    return defer.fail(Exception(f'Incompatible sync service: {sync_service}'))
                else:
                    return threads.deferToThread(sync_service.sip_notify, ip, 'check-sync')

    def get_remote_state_trigger_filename(self, device):
        if 'mac' not in device:
            return None

        return self._dev_specific_filename(device)

    def is_sensitive_filename(self, filename):
        return bool(self._SENSITIVE_FILENAME_REGEX.match(filename))
