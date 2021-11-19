# -*- coding: utf-8 -*-

# Copyright 2016-2019 The Wazo Authors  (see the AUTHORS file)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import logging
import re
import os.path

from operator import itemgetter
from provd import tzinform
from provd import synchronize
from provd.plugins import StandardPlugin, FetchfwPluginHelper, \
    TemplatePluginHelper
from provd.devices.pgasso import IMPROBABLE_SUPPORT, COMPLETE_SUPPORT, \
    FULL_SUPPORT, BasePgAssociator, UNKNOWN_SUPPORT
from provd.servers.http import HTTPNoListingFileService
from provd.util import norm_mac, format_mac
from twisted.internet import defer, threads

logger = logging.getLogger('plugin.wazo-patton')


class BasePattonHTTPDeviceInfoExtractor(object):

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
                return {u'vendor': u'Patton',
                        u'model': raw_model.decode('ascii'),
                        u'version': raw_version.decode('ascii'),
                        u'mac': mac}
        return None


class BasePattonPgAssociator(BasePgAssociator):

    def __init__(self, models, version):
        self._models = models
        self._version = version

    def _do_associate(self, vendor, model, version):
        if vendor == u'Patton':
            if model in self._models:
                if version == self._version:
                    return FULL_SUPPORT
                return COMPLETE_SUPPORT
            return UNKNOWN_SUPPORT
        return IMPROBABLE_SUPPORT


class _TimezoneConverter(object):

    _DAYS_DEFAULT_SUFFIX = u'th'
    _DAYS_SUFFIX = {
        1: u'st',
        2: u'nd',
        3: u'rd',
        11: u'st',
        12: u'nd',
        13: u'rd',
        21: u'st',
        22: u'nd',
        23: u'rd',
        31: u'st',
    }
    _DAYS_OF_WEEK = [
        u'monday',
        u'tuesday',
        u'wednesday',
        u'thursday',
        u'friday',
        u'saturday',
        u'sunday',
    ]
    _MONTHS = [
        u'jan',
        u'feb',
        u'mar',
        u'apr',
        u'may',
        u'jun',
        u'jul',
        u'aug',
        u'sep',
        u'oct',
        u'nov',
        u'dec',
    ]
    _WEEKS = [
        u'first',
        u'second',
        u'third',
        u'fourth',
        u'last',
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
        return u'%02d:%02d' % (hours, minutes)

    def _format_time_as_offset(self, tz_time):
        hours, minutes, _ = tz_time.as_hms
        if hours < 0 or minutes < 0:
            sign = u'-'
        else:
            sign = u'+'
        return u'%s%02d:%02d' % (sign, abs(hours), abs(minutes))

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
            day_rule = u'%s %s' % (fmted_week, fmted_day_of_week)
        return u'%s %s %s' % (fmted_time, fmted_month, day_rule)

    def _convert_day(self, day):
        suffix = self._DAYS_SUFFIX.get(day, self._DAYS_DEFAULT_SUFFIX)
        return u'%d%s' % (day, suffix)

    def _convert_day_of_week(self, day_of_week):
        return self._DAYS_OF_WEEK[tzinform.week_start_on_monday(day_of_week) - 1]

    def _convert_month(self, month):
        return self._MONTHS[month - 1]

    def _convert_week(self, week):
        return self._WEEKS[week - 1]


class _SIPLinesConverter(object):

    def __init__(self):
        self._lines = []
        self._servers = []
        self._next_server_id = 1

    def add_sip_line(self, sip_line_no, sip_line):
        line = self._build_line(sip_line_no, sip_line)
        server = self._build_server(sip_line, u'proxy_ip', u'proxy_port')
        if u'backup_proxy_ip' in sip_line:
            backup_server = self._build_server(sip_line, u'backup_proxy_ip', u'backup_proxy_port')
        else:
            backup_server = None

        line[u'servers'].append(server)
        server[u'lines'].append(line)
        if backup_server is not None:
            line[u'servers'].append(backup_server)
            backup_server[u'lines'].append(line)

    def _build_line(self, sip_line_no, sip_line):
        line_no = int(sip_line_no)
        username = sip_line[u'username']
        for existing_line in self._lines:
            if existing_line[u'username'] == username:
                raise Exception(u'username %s is referenced by both lines %s and %s' % (
                                username, line_no, existing_line[u'line_no']))
        line = self._new_line(line_no, sip_line)
        self._lines.append(line)
        return line

    def _new_line(self, line_no, sip_line):
        line = {
            u'line_no': line_no,
            u'fxs_port_no': line_no - 1,
            u'auth_username': sip_line[u'auth_username'],
            u'username': sip_line[u'username'],
            u'password': sip_line[u'password'],
            u'proxy_ip': sip_line[u'proxy_ip'],
            u'registrar_ip': sip_line.get(u'registrar_ip', sip_line[u'proxy_ip']),
            u'registrar_port': sip_line.get(u'registrar_port', u'5060'),
            u'servers': [],
        }
        if u'backup_proxy_ip' in sip_line:
            line[u'backup_registrar_ip'] = sip_line.get(u'backup_registrar_ip', sip_line[u'backup_proxy_ip'])
            line[u'backup_registrar_port'] = sip_line.get(u'backup_registrar_port', u'5060')
        return line

    def _build_server(self, sip_line, key_proxy_ip, key_proxy_port):
        proxy_ip = sip_line[key_proxy_ip]
        proxy_port = sip_line.get(key_proxy_port, u'5060')
        for existing_server in self._servers:
            if existing_server[u'proxy_ip'] == proxy_ip:
                if existing_server[u'proxy_port'] != proxy_port:
                    raise Exception(u'proxy %s is referenced with both port %s and %s' % (
                                    proxy_ip, proxy_port, existing_server[u'proxy_port']))
                return existing_server
        server = self._new_server(proxy_ip, proxy_port)
        self._servers.append(server)
        return server

    def _new_server(self, proxy_ip, proxy_port):
        server = {
            u'id': self._next_server_id,
            u'proxy_ip': proxy_ip,
            u'proxy_port': proxy_port,
            u'lines': [],
        }
        self._next_server_id += 1
        return server

    def lines(self):
        return sorted(self._lines, key=itemgetter(u'line_no'))

    def servers(self):
        return list(self._servers)


class BasePattonPlugin(StandardPlugin):

    _ENCODING = 'ascii'
    _SIP_DTMF_MODE = {
        u'RTP-in-band': u'default',
        u'RTP-out-of-band': u'rtp',
        u'SIP-INFO': u'signaling'
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
        if u'syslog_level' in raw_config:
            if raw_config[u'syslog_level'] == u'info':
                raw_config[u'XX_syslog_level'] = u'informational'
            else:
                raw_config[u'XX_syslog_level'] = raw_config[u'syslog_level']

    def _add_timezone_and_dst(self, raw_config):
        if u'timezone' in raw_config:
            try:
                tzinfo = tzinform.get_timezone_info(raw_config[u'timezone'])
            except tzinform.TimezoneNotFoundError as e:
                logger.info('Unknown timezone: %s', e)
            else:
                converter = _TimezoneConverter(tzinfo)
                raw_config[u'XX_timezone_offset'] = converter.default_offset()
                if converter.has_dst():
                    raw_config[u'XX_dst_offset'] = converter.dst_offset()
                    raw_config[u'XX_dst_start'] = converter.dst_start()
                    raw_config[u'XX_dst_end'] = converter.dst_end()

    def _update_sip_transport(self, raw_config):
        if u'sip_transport' not in raw_config:
            raw_config[u'sip_transport'] = u'udp'
        elif raw_config.get(u'sip_transport') == u'tls':
            logger.warning("Patton doesn't support the SIP transport tls: fallback to udp")
            raw_config[u'sip_transport'] = u'udp'

    def _add_dtmf_relay(self, raw_config):
        if u'sip_dtmf_mode' in raw_config:
            raw_config[u'XX_dtmf_relay'] = self._SIP_DTMF_MODE[raw_config[u'sip_dtmf_mode']]

    def _add_lines_and_servers(self, raw_config):
        converter = _SIPLinesConverter()
        for sip_line_no, sip_line in raw_config[u'sip_lines'].iteritems():
            converter.add_sip_line(sip_line_no, sip_line)
        raw_config[u'XX_lines'] = converter.lines()
        raw_config[u'XX_servers'] = converter.servers()

    _SENSITIVE_FILENAME_REGEX = re.compile(r'^[0-9a-f]{12}\.cfg$')

    def _dev_specific_filename(self, device):
        fmted_mac = format_mac(device[u'mac'], separator='')
        return fmted_mac + '.cfg'

    def _check_device(self, device):
        if u'mac' not in device:
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
                ip = device[u'ip'].encode('ascii')
            except KeyError:
                return defer.fail(Exception('IP address needed for device synchronization'))
            else:
                sync_service = synchronize.get_sync_service()
                if sync_service is None or sync_service.TYPE != 'AsteriskAMI':
                    return defer.fail(Exception('Incompatible sync service: %s' % sync_service))
                else:
                    return threads.deferToThread(sync_service.sip_notify, ip, 'check-sync')

    def get_remote_state_trigger_filename(self, device):
        if u'mac' not in device:
            return None

        return self._dev_specific_filename(device)

    def is_sensitive_filename(self, filename):
        return bool(self._SENSITIVE_FILENAME_REGEX.match(filename))
