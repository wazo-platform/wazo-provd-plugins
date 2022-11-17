# Copyright 2010-2022 The Wazo Authors  (see the AUTHORS file)
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
from __future__ import annotations

import logging
import re
import os.path
from operator import itemgetter
from typing import Dict, Optional
from xml.sax.saxutils import escape
from provd import tzinform
from provd import synchronize
from provd.devices.config import RawConfigError
from provd.devices.pgasso import BasePgAssociator, DeviceSupport
from provd.plugins import StandardPlugin, FetchfwPluginHelper, TemplatePluginHelper
from provd.servers.http import HTTPNoListingFileService
from provd.util import norm_mac, format_mac
from provd.servers.http_site import Request
from provd.devices.ident import RequestType
from twisted.internet import defer

logger = logging.getLogger('plugin.wazo-polycom')


class BasePolycomHTTPDeviceInfoExtractor:
    _UA_REGEX = re.compile(r'^FileTransport Polycom\w+-(\w*?)-UA/([\d.]+)')
    _PATH_REGEX = re.compile(
        r'/(?!000000000000)([\da-f]{12})'
        r'(?:\.cfg|-boot\.log|-phone\.cfg|-license\.cfg|-directory\.xml|-app\.log)$'
    )
    _IS_SIPAPP_REGEX = re.compile(
        r'/(?:(?:common\.cfg|phone1\.cfg|sip\.cfg)|'
        r'(?:[\da-f]{12}-(?:phone\.cfg|license\.cfg|directory\.xml|app\.log)))$'
    )

    def extract(self, request: Request, request_type: RequestType):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request: Request):
        ua = request.getHeader(b'User-Agent')
        if ua:
            dev_info = {}
            self._extract_info_from_ua(ua.decode('ascii'), dev_info)
            if dev_info:
                path = request.path.decode('ascii')
                if 'version' in dev_info and not self._is_sip_application_request(path):
                    del dev_info['version']
                self._extract_mac_from_path(path, dev_info)
                return dev_info
        return None

    def _extract_info_from_ua(self, ua: str, dev_info: Dict[str, str]):
        # Note: depending on the boot step, the version number will either
        # be the BootROM version (first few requests) or the SIP application
        # version (later on in the boot process).
        # HTTP User-Agent:
        #   "FileTransport PolycomSoundPointIP-SPIP_335-UA/3.2.1.0078"
        #   (SPIP335 3.2.1.0078/4.2.1.0275)
        #   "FileTransport PolycomSoundPointIP-SPIP_335-UA/4.2.1.0275"
        #   (SPIP335 3.2.1.0078/4.2.1.0275)
        #   "FileTransport PolycomSoundPointIP-SPIP_450-UA/3.2.3.1734"
        #   (SPIP450 3.2.3.1734/4.2.2.0710)
        #   "FileTransport PolycomSoundPointIP-SPIP_550-UA/3.2.3.1734"
        #   (SPIP335 3.2.3.1734/4.2.2.0710)
        #   "FileTransport PolycomSoundStationIP-SSIP_6000-UA/4.0.4.2906 Type/Application"
        #   "FileTransport PolycomSoundStationIP-SSIP_6000-UA/5.0.3.1667 Type/Updater"
        m = self._UA_REGEX.match(ua)
        if m:
            dev_info['vendor'] = 'Polycom'
            raw_model, raw_version = m.groups()
            dev_info['model'] = raw_model.replace('_', '')
            dev_info['version'] = raw_version

    def _extract_mac_from_path(self, path: str, dev_info: Dict[str, str]):
        # Extract the MAC address from the requested path if possible
        m = self._PATH_REGEX.search(path)
        if m:
            raw_mac = m.group(1)
            dev_info['mac'] = norm_mac(raw_mac)

    def _is_sip_application_request(self, path: str) -> bool:
        # Return true if path has been requested by the SIP application (and
        # not the BootROM). This use the fact that some files are only
        # request by the SIP application.
        return bool(self._IS_SIPAPP_REGEX.search(path))


class BasePolycomPgAssociator(BasePgAssociator):
    def __init__(self, models, version):
        super().__init__()
        self._models = models
        self._version = version

    def _do_associate(
        self, vendor: str, model: Optional[str], version: Optional[str]
    ) -> DeviceSupport:
        if vendor == 'Polycom':
            if model in self._models:
                if version == self._version:
                    return DeviceSupport.EXACT
                return DeviceSupport.COMPLETE
            return DeviceSupport.PROBABLE
        return DeviceSupport.IMPROBABLE


class BasePolycomPlugin(StandardPlugin):
    # Note that no TFTP support is included since Polycom phones are capable of
    # protocol selection via DHCP options.
    _ENCODING = 'UTF-8'
    _NB_FKEY = {
        'SPIP450': 2,
        'SPIP550': 3,
        'SPIP560': 3,
        'SPIP650': 47,
        'SPIP670': 47,
    }
    _LOCALE = {
        'de_DE': 'German_Germany',
        'en_US': 'English_United_States',
        'es_ES': 'Spanish_Spain',
        'fr_FR': 'French_France',
        'fr_CA': 'French_France',
        'it_IT': 'Italian_Italy',
        'nl_NL': 'Dutch_Netherlands',
    }
    _SYSLOG_LEVEL = {
        'critical': '5',
        'error': '4',
        'warning': '3',
        'info': '2',
        'debug': '1',
    }
    _SYSLOG_LEVEL_DEF = '1'
    _SIP_TRANSPORT = {'udp': 'UDPOnly', 'tcp': 'TCPOnly', 'tls': 'TLS'}
    _SIP_TRANSPORT_DEF = 'UDPOnly'

    def __init__(self, app, plugin_dir, gen_cfg, spec_cfg):
        super().__init__(app, plugin_dir, gen_cfg, spec_cfg)

        self._tpl_helper = TemplatePluginHelper(plugin_dir)

        downloaders = FetchfwPluginHelper.new_downloaders(gen_cfg.get('proxies'))
        fetchfw_helper = FetchfwPluginHelper(plugin_dir, downloaders)

        self.services = fetchfw_helper.services()
        self.http_service = HTTPNoListingFileService(self._tftpboot_dir)

    http_dev_info_extractor = BasePolycomHTTPDeviceInfoExtractor()

    def _format_dst_change(self, suffix, dst_change):
        lines = []
        lines.append(
            f'tcpIpApp.sntp.daylightSavings.{suffix}.month="{dst_change["month"]:d}"'
        )
        lines.append(
            f'tcpIpApp.sntp.daylightSavings.{suffix}.time="{dst_change["time"].as_hours:d}"'
        )
        if dst_change['day'].startswith('D'):
            lines.append(
                f'tcpIpApp.sntp.daylightSavings.{suffix}.date="{dst_change["day"][1:]}"'
            )
        else:
            week, weekday = dst_change['day'][1:].split('.')
            lines.append(
                f'tcpIpApp.sntp.daylightSavings.{suffix}.dayOfWeek="{weekday}"'
            )
            if week == '5':
                lines.append(
                    f'tcpIpApp.sntp.daylightSavings.{suffix}.dayOfWeek.lastInMonth="1"'
                )
            else:
                lines.append(
                    f'tcpIpApp.sntp.daylightSavings.{suffix}.dayOfWeek.lastInMonth="0"'
                )
                lines.append(
                    f'tcpIpApp.sntp.daylightSavings.{suffix}.date="{(int(week) - 1) * 7 + 1:d}"'
                )
        return lines

    def _format_tzinfo(self, tzinfo):
        lines = []
        lines.append(f'tcpIpApp.sntp.gmtOffset="{tzinfo["utcoffset"].as_seconds:d}"')
        if tzinfo['dst'] is None:
            lines.append('tcpIpApp.sntp.daylightSavings.enable="0"')
        else:
            lines.append('tcpIpApp.sntp.daylightSavings.enable="1"')
            if tzinfo['dst']['start']['day'].startswith('D'):
                lines.append('tcpIpApp.sntp.daylightSavings.fixedDayEnable="1"')
            else:
                lines.append('tcpIpApp.sntp.daylightSavings.fixedDayEnable="0"')
            lines.extend(self._format_dst_change('start', tzinfo['dst']['start']))
            lines.extend(self._format_dst_change('stop', tzinfo['dst']['end']))
        return '\n'.join(lines)

    def _add_timezone(self, raw_config):
        if 'timezone' in raw_config:
            try:
                tzinfo = tzinform.get_timezone_info(raw_config['timezone'])
            except tzinform.TimezoneNotFoundError as e:
                logger.info('Unknown timezone: %s', e)
            else:
                raw_config['XX_timezone'] = self._format_tzinfo(tzinfo)

    def _add_language(self, raw_config):
        locale = raw_config.get('locale')
        if locale in self._LOCALE:
            raw_config['XX_language'] = self._LOCALE[locale]

    def _add_fkeys(self, raw_config, model):
        if model not in self._NB_FKEY:
            logger.info('Unknown model or model with no funckeys: %s', model)
            return
        nb_keys = self._NB_FKEY[model]
        lines = []
        for funckey_no, funckey_dict in sorted(
            iter(raw_config['funckeys'].items()), key=itemgetter(0)
        ):
            funckey_type = funckey_dict['type']
            if funckey_type == 'speeddial':
                logger.info('Polycom doesn\'t support non-supervised function keys')
            elif funckey_type != 'blf':
                logger.info('Unsupported funckey type: %s', funckey_type)
                continue
            keynum = int(funckey_no)
            if keynum <= nb_keys:
                value = funckey_dict['value']
                lines.append(
                    'attendant.resourceList.%s.address="%s"' % (funckey_no, value)
                )
                lines.append(
                    'attendant.resourceList.%s.label="%s"'
                    % (funckey_no, escape(funckey_dict.get('label', value)))
                )
            else:
                logger.info(
                    'Model %s has less than %s function keys', model, funckey_no
                )
        raw_config['XX_fkeys'] = '\n'.join(lines)

    def _add_syslog_level(self, raw_config):
        syslog_level = raw_config.get('syslog_level')
        raw_config['XX_syslog_level'] = self._SYSLOG_LEVEL.get(
            syslog_level, self._SYSLOG_LEVEL_DEF
        )

    def _add_sip_transport(self, raw_config):
        raw_config['XX_sip_transport'] = self._SIP_TRANSPORT.get(
            raw_config.get('sip_transport'), self._SIP_TRANSPORT_DEF
        )

    def _update_sip_lines(self, raw_config):
        proxy_ip = raw_config.get('sip_proxy_ip')
        proxy_port = raw_config.get('sip_proxy_port', '')
        backup_proxy_ip = raw_config.get('sip_backup_proxy_ip', '')
        backup_proxy_port = raw_config.get('sip_backup_proxy_port', '')
        voicemail = raw_config.get('exten_voicemail')
        for line in raw_config['sip_lines'].values():
            line.setdefault('proxy_ip', proxy_ip)
            line.setdefault('proxy_port', proxy_port)
            line.setdefault('backup_proxy_ip', backup_proxy_ip)
            line.setdefault('backup_proxy_port', backup_proxy_port)
            if voicemail:
                line.setdefault('voicemail', voicemail)

    def _dev_specific_filename(self, device: Dict[str, str]) -> str:
        # Return the device specific filename (not pathname) of device
        formatted_mac = format_mac(device['mac'], separator='')
        return f'{formatted_mac}-user.cfg'

    def _check_config(self, raw_config):
        if 'http_port' not in raw_config:
            raise RawConfigError('only support configuration via HTTP')

    def _check_device(self, device):
        if 'mac' not in device:
            raise Exception('MAC address needed for device configuration')

    def configure(self, device, raw_config):
        self._check_config(raw_config)
        self._check_device(device)
        filename = self._dev_specific_filename(device)
        tpl = self._tpl_helper.get_dev_template(filename, device)

        self._add_timezone(raw_config)
        self._add_language(raw_config)
        self._add_fkeys(raw_config, device.get('model'))
        self._add_syslog_level(raw_config)
        self._add_sip_transport(raw_config)
        self._update_sip_lines(raw_config)

        path = os.path.join(self._tftpboot_dir, filename)
        self._tpl_helper.dump(tpl, raw_config, path, self._ENCODING)

    def deconfigure(self, device):
        path = os.path.join(self._tftpboot_dir, self._dev_specific_filename(device))
        try:
            os.remove(path)
        except OSError as e:
            logger.warning('error while deconfiguring device: %s', e)

    def synchronize(self, device, raw_config):
        return synchronize.standard_sip_synchronize(device)

    def get_remote_state_trigger_filename(self, device):
        if 'mac' not in device:
            return None
        return self._dev_specific_filename(device)
