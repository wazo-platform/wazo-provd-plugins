# Copyright 2011-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

"""Common code shared by the various wazo-alcatel plugins.

Support the IP Touch 4028EE, 4038EE & 4068EE.

"""
from __future__ import annotations

import calendar
import datetime
import logging
import os.path
import re
import time

try:
    from wazo_provd import tzinform
    from wazo_provd.devices.config import RawConfigError
    from wazo_provd.devices.ident import RequestType
    from wazo_provd.devices.pgasso import BasePgAssociator, DeviceSupport
    from wazo_provd.plugins import (
        FetchfwPluginHelper,
        StandardPlugin,
        TemplatePluginHelper,
    )
    from wazo_provd.servers.http import HTTPNoListingFileService
    from wazo_provd.servers.http_site import Request
    from wazo_provd.servers.tftp.service import TFTPFileService, TFTPRequest
    from wazo_provd.util import format_mac, norm_mac
except ImportError:
    # Compatibility with wazo < 24.02
    from provd import tzinform
    from provd.devices.config import RawConfigError
    from provd.devices.ident import RequestType
    from provd.devices.pgasso import BasePgAssociator, DeviceSupport
    from provd.plugins import FetchfwPluginHelper, StandardPlugin, TemplatePluginHelper
    from provd.servers.http import HTTPNoListingFileService
    from provd.servers.http_site import Request
    from provd.servers.tftp.service import TFTPFileService, TFTPRequest
    from provd.util import format_mac, norm_mac

from twisted.internet import defer, threads

logger = logging.getLogger('plugin.wazo-alcatel')

VENDOR = 'Alcatel'


class BaseAlcatelHTTPDeviceInfoExtractor:
    _UA_REGEX = re.compile(r'^Alcatel IP Touch (\d+)/([\w.]+)$')
    _PATH_REGEX = re.compile(r'\bsipconfig-(\w+)\.txt$')

    def extract(self, request: Request, request_type: RequestType):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request: Request):
        ua = request.getHeader(b'User-Agent')
        if ua:
            dev_info = self._extract_from_ua(ua.decode('ascii'))
            if dev_info:
                self._extract_from_path(request.path.decode('ascii'), dev_info)
            return dev_info
        return None

    def _extract_from_ua(self, ua: str):
        # Note that the MAC address if not present in User-Agent and so will
        # never be returned by this function.
        # HTTP User-Agent:
        #   "Alcatel IP Touch 4028/2.01.20"
        #   "Alcatel IP Touch 4038/2.01.20"
        #   "Alcatel IP Touch 4068/2.01.20"
        m = self._UA_REGEX.match(ua)
        if m:
            model, version = m.groups()
            return {
                'vendor': VENDOR,
                'model': model,
                'version': version,
            }
        return None

    def _extract_from_path(self, path: str, dev_info: dict[str, str]):
        # try to extract MAC address from path
        m = self._PATH_REGEX.search(path)
        if m:
            raw_mac = m.group(1)
            try:
                mac = norm_mac(raw_mac)
            except ValueError as e:
                logger.warning('Could not normalize MAC address: %s', e)
            else:
                dev_info['mac'] = mac


class BaseAlcatelTFTPDeviceInfoExtractor:
    # We need a TFTP device extractor if we want to be able to update a phone
    # in NOE mode to SIP mode, since it seems like it's not possible for the
    # phone to do HTTP request in NOE mode

    def extract(self, request: TFTPRequest, request_type: RequestType):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request: TFTPRequest):
        filename = request['packet']['filename']
        if filename == b'/lanpbx.cfg':
            return {'vendor': VENDOR}
        return None


class BaseAlcatelPgAssociator(BasePgAssociator):
    def __init__(self, models, version):
        self._models = models
        self._version = version

    def _do_associate(
        self, vendor: str, model: str | None, version: str | None
    ) -> DeviceSupport:
        if vendor == VENDOR:
            if model in self._models:
                if version == self._version:
                    return DeviceSupport.EXACT
                return DeviceSupport.COMPLETE
            return DeviceSupport.PROBABLE
        return DeviceSupport.IMPROBABLE


class BaseAlcatelPlugin(StandardPlugin):
    _ENCODING = 'UTF-8'
    _DEFAULT_PASSWORD = '000000'
    _SIP_TRANSPORT = {'udp': '1', 'tcp': '2'}
    _SIP_DTMF_MODE = {'RTP-in-band': '1', 'RTP-out-of-band': '0', 'SIP-INFO': '2'}
    _NB_FKEYS = {'4028': 4, '4038': 6, '4068': 8}
    # XXX this is confused, but I don't care that much right now
    _TONE_COUNTRY: list[list[str]] = [
        # "English" tone country
        ['US', 'CA'],
        # "French" tone country
        ['FR'],
        # "German" tone country
        ['DE'],
        # "Italian" tone country
        ['IT'],
        # "Spanish" tone country
        ['ES'],
        # "Dutch" tone country
        [],
        # "Portuguese" tone country
        [],
    ]

    def __init__(self, app, plugin_dir, gen_cfg, spec_cfg):
        super().__init__(app, plugin_dir, gen_cfg, spec_cfg)

        self._tpl_helper = TemplatePluginHelper(plugin_dir)

        downloaders = FetchfwPluginHelper.new_downloaders(gen_cfg.get('proxies'))
        fetchfw_helper = FetchfwPluginHelper(plugin_dir, downloaders)

        self.services = fetchfw_helper.services()
        self.http_service = HTTPNoListingFileService(self._tftpboot_dir)
        self.tftp_service = TFTPFileService(self._tftpboot_dir)

    http_dev_info_extractor = BaseAlcatelHTTPDeviceInfoExtractor()

    tftp_dev_info_extractor = BaseAlcatelTFTPDeviceInfoExtractor()

    def _extract_sip_line_info(self, raw_config):
        assert raw_config['sip_lines']
        sip_lines_key = min(raw_config['sip_lines'])
        sip_line = raw_config['sip_lines'][sip_lines_key]

        def set_if(line_id, id):
            if line_id in sip_line:
                raw_config[id] = sip_line[line_id]

        set_if('proxy_ip', 'sip_proxy_ip')
        set_if('proxy_port', 'sip_proxy_port')
        set_if('backup_proxy_ip', 'sip_backup_proxy_ip')
        set_if('backup_proxy_port', 'sip_backup_proxy_port')
        set_if('outbound_proxy_ip', 'sip_outbound_proxy_ip')
        set_if('outbound_proxy_port', 'sip_outbound_proxy_port')
        set_if('registrar_ip', 'sip_registrar_ip')
        set_if('registrar_port', 'sip_registrar_port')
        set_if('backup_registrar_ip', 'sip_backup_registrar_ip')
        set_if('backup_registrar_port', 'sip_backup_registrar_port')

        raw_config['XX_auth_name'] = sip_line['auth_username']
        raw_config['XX_auth_password'] = sip_line['password']
        raw_config['XX_user_name'] = sip_line['username']
        raw_config['XX_display_name'] = sip_line['display_name']

        voicemail = sip_line.get('voicemail') or raw_config.get('exten_voicemail')
        if voicemail:
            raw_config['XX_voice_mail_uri'] = voicemail
            # XXX should we consider the value of sip_subscribe_mwi before ?
            raw_config['XX_mwi_uri'] = f"{voicemail}@{raw_config['sip_proxy_ip']}"

    def _add_dns_addr(self, raw_config):
        # this function must be called after _extract_sip_line_info
        # bypass DNS if not enabled to Google DNS issues, because Wazo EUC
        # does not provide IP DNS server configuration for the phones
        if raw_config.get('dns_enabled'):
            dns_addr = raw_config['dns_ip']
        else:
            dns_addr = '8.8.8.8'
        raw_config['XX_dns_addr'] = dns_addr

    def _add_sip_transport_mode(self, raw_config):
        try:
            sip_transport = self._SIP_TRANSPORT[raw_config['sip_transport']]
        except KeyError:
            logger.info(
                'Unknown/unsupported sip_transport: %s', raw_config['sip_transport']
            )
        else:
            raw_config['XX_sip_transport_mode'] = sip_transport

    def _add_sntp_addr(self, raw_config):
        if raw_config.get('ntp_enabled'):
            raw_config['XX_sntp_addr'] = raw_config['ntp_ip']

    def _format_dst_change(self, dst):
        if dst['day'].startswith('D'):
            day = int(dst['day'][1:])
        else:
            # compute the day of the month for the current year
            raw_week, raw_weekday = dst['day'][1:].split('.')
            week = int(raw_week) - 1
            weekday = tzinform.week_start_on_monday(int(raw_weekday)) - 1
            current_year = datetime.datetime.utcnow().year
            month_calendar = calendar.monthcalendar(current_year, dst['month'])
            day = month_calendar[week][weekday]
        return f'{dst["month"]:02d}{day:02d}{dst["time"].as_hours:02d}'

    def _format_tzinfo(self, tzinfo):
        offset = tzinfo['utcoffset'].as_minutes
        if tzinfo['dst']:
            dst_start = self._format_dst_change(tzinfo['dst']['start'])
            dst_end = self._format_dst_change(tzinfo['dst']['end'])
        else:
            dst_start = '000000'
            dst_end = '000000'
        return f'UT::{offset}:{dst_start}:{dst_end}'

    def _add_timezone(self, raw_config):
        if 'timezone' in raw_config:
            try:
                tzinfo = tzinform.get_timezone_info(raw_config['timezone'])
            except tzinform.TimezoneNotFoundError as e:
                logger.info('Unknown timezone: %s', e)
            else:
                try:
                    raw_config['XX_timezone'] = self._format_tzinfo(tzinfo)
                except Exception:
                    logger.error('Error while formating tzinfo', exc_info=True)

    def _add_tone_country(self, raw_config) -> None:
        if 'locale' in raw_config:
            try:
                country: str = raw_config['locale'].rsplit('_', 1)[1]
            except IndexError:
                # locale is not of the form 'xx_XX'
                return None
            for i, countries in enumerate(self._TONE_COUNTRY):
                if country in countries:
                    raw_config['XX_tone_country'] = str(i)
                    break

    def _add_dtmf_type(self, raw_config):
        if 'sip_dtmf_mode' in raw_config:
            try:
                dtmf_type = self._SIP_DTMF_MODE[raw_config['sip_dtmf_mode']]
            except KeyError:
                logger.info(
                    'Unknown/unsupported sip_dtmf_mode: %s', raw_config['sip_dtmf_mode']
                )
            else:
                raw_config['XX_dtmf_type'] = dtmf_type

    def _add_fkeys(self, raw_config, device):
        lines = []
        model = device.get('model')
        nb_fkeys = self._NB_FKEYS.get(model, 8)
        for funckey_no, funckey_dict in raw_config['funckeys'].items():
            int_funckey_no = int(funckey_no)
            if int_funckey_no > nb_fkeys:
                logger.warning(
                    'Out of range funckey number for model %s: %s (max: %s)',
                    model,
                    funckey_no,
                    nb_fkeys,
                )
            else:
                funckey_type = funckey_dict['type']
                if funckey_type == 'speeddial':
                    value = funckey_dict['value']
                    # need to set a non-empty label for the funckey to works
                    label = funckey_dict.get('label', value)
                    lines.append(f'speed_dial_{funckey_no}_first_name={label}')
                    lines.append(f'speed_dial_{funckey_no}_uri={value}')
                else:
                    logger.warning('Unsupported funckey type: %s', funckey_type)
        raw_config['XX_fkeys'] = '\n'.join(lines)

    def _update_admin_password(self, raw_config):
        password = raw_config.get('admin_password', self._DEFAULT_PASSWORD)
        # ensure password is digits only
        if not password.isdigit():
            logger.warning(
                'admin_password contains non-digit characters, using default password'
            )
            password = self._DEFAULT_PASSWORD
        raw_config['admin_password'] = password

    def _dev_specific_filename(self, device: dict[str, str]) -> str:
        # Return the device specific filename (not pathname) of device
        formatted_mac = format_mac(device['mac'], separator='', uppercase=False)
        return f'sipconfig-{formatted_mac}.txt'

    def _check_config(self, raw_config):
        if 'http_port' not in raw_config:
            raise RawConfigError('only support configuration via HTTP')
        if not raw_config['sip_lines']:
            # the phone won't be configured properly if a sip line is not defined
            raise RawConfigError('need at least one sip lines defined')

    def _check_device(self, device):
        if 'mac' not in device:
            raise Exception('MAC address needed for device configuration')

    def configure(self, device, raw_config):
        self._check_config(raw_config)
        self._check_device(device)
        filename = self._dev_specific_filename(device)
        tpl = self._tpl_helper.get_dev_template(filename, device)

        self._extract_sip_line_info(raw_config)
        self._add_dns_addr(raw_config)
        self._add_sip_transport_mode(raw_config)
        self._add_sntp_addr(raw_config)
        self._add_timezone(raw_config)
        self._add_tone_country(raw_config)
        self._add_dtmf_type(raw_config)
        self._add_fkeys(raw_config, device)
        self._update_admin_password(raw_config)

        path = os.path.join(self._tftpboot_dir, filename)
        self._tpl_helper.dump(tpl, raw_config, path, self._ENCODING)

    def deconfigure(self, device):
        path = os.path.join(self._tftpboot_dir, self._dev_specific_filename(device))
        try:
            os.remove(path)
        except OSError as e:
            # ignore
            logger.info('error while removing file: %s', e)

    def _do_synchronize_via_telnet(self, ip, password):
        import pexpect

        child = pexpect.spawn('telnet', [ip], timeout=5)
        try:
            child.expect('Password ?')
            child.sendline(password)
            child.expect('Login accepted')
            child.sendline('reset soft')
            # wait a short time before closing the connection
            time.sleep(10)
        finally:
            child.close(force=True)

    def synchronize(self, device, raw_config):
        try:
            ip = device['ip'].encode('ascii')
        except KeyError:
            return defer.fail(Exception('IP address needed for device synchronization'))
        else:
            password = raw_config.get('admin_password', self._DEFAULT_PASSWORD).encode(
                'ascii'
            )
            return threads.deferToThread(self._do_synchronize_via_telnet, ip, password)

    def get_remote_state_trigger_filename(self, device):
        if 'mac' not in device:
            return None

        return self._dev_specific_filename(device)
