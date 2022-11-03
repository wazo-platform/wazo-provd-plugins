# Copyright 2010-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+
from __future__ import annotations

import logging
import os
import re
from typing import Dict, Optional, Union

from provd import plugins
from provd import tzinform
from provd.devices.config import RawConfigError
from provd.devices.pgasso import BasePgAssociator, DeviceSupport
from provd.plugins import StandardPlugin, FetchfwPluginHelper, TemplatePluginHelper
from provd.servers.http import HTTPNoListingFileService
from provd.servers.tftp.service import TFTPFileService
from provd.util import norm_mac, format_mac
from provd.servers.http_site import Request
from provd.devices.ident import RequestType
from twisted.internet import defer

logger = logging.getLogger('plugin.wazo-cisco')


class BaseCiscoPgAssociator(BasePgAssociator):
    def __init__(self, models):
        self._models = models

    def _do_associate(
        self, vendor: str, model: Optional[str], version: Optional[str]
    ) -> Union[DeviceSupport, int]:
        if vendor == 'Cisco':
            if model is None:
                # when model is None, give a score slightly higher than
                # wazo-cisco-spa plugins
                return DeviceSupport.PROBABLE.value + 10
            if model.startswith('SPA') or model.startswith('ATA'):
                return DeviceSupport.NONE
            if model in self._models:
                return DeviceSupport.COMPLETE
            return DeviceSupport.PROBABLE
        return DeviceSupport.IMPROBABLE


class BaseCiscoDHCPDeviceInfoExtractor:
    def extract(self, request: dict, request_type: RequestType):
        return defer.succeed(self._do_extract(request))

    _VDI_REGEX = re.compile(r'\bPhone (?:79(\d\d)|CP-79(\d\d)G|CP-(\d\d\d\d))')

    def _do_extract(self, request):
        options = request['options']
        if 60 in options:
            return self._extract_from_vdi(options[60])

    def _extract_from_vdi(self, vdi):
        # Vendor class identifier:
        #   "Cisco Systems, Inc." (Cisco 6901 9.1.2/9.2.1)
        #   "Cisco Systems, Inc. IP Phone 7912" (Cisco 7912 9.0.3)
        #   "Cisco Systems, Inc. IP Phone CP-7940G\x00" (Cisco 7940 8.1.2)
        #   "Cisco Systems, Inc. IP Phone CP-7941G\x00" (Cisco 7941 9.0.3)
        #   "Cisco Systems, Inc. IP Phone CP-7960G\x00" (Cisco 7960 8.1.2)
        #   "Cisco Systems, Inc. IP Phone CP-8961\x00" (Cisco 8961 9.1.2)
        #   "Cisco Systems, Inc. IP Phone CP-9951\x00" (Cisco 9951 9.1.2)
        #   "Cisco Systems Inc. Wireless Phone 7921"
        if vdi.startswith('Cisco Systems'):
            dev_info = {'vendor': 'Cisco'}
            m = self._VDI_REGEX.search(vdi)
            if m:
                _7900_modelnum = m.group(1) or m.group(2)
                if _7900_modelnum:
                    if _7900_modelnum == '20':
                        fmt = '79%s'
                    else:
                        fmt = '79%sG'
                    dev_info['model'] = fmt % _7900_modelnum
                else:
                    model_num = m.group(3)
                    dev_info['model'] = model_num
            return dev_info


class BaseCiscoHTTPDeviceInfoExtractor:
    _CIPC_REGEX = re.compile(r'^/Communicator[/\\]')
    _FILENAME_REGEXES = [
        re.compile(r'^/SEP([\dA-F]{12})\.cnf\.xml$'),
        re.compile(r'^/CTLSEP([\dA-F]{12})\.tlv$'),
        re.compile(r'^/ITLSEP([\dA-F]{12})\.tlv$'),
        re.compile(r'^/ITLFile\.tlv$'),
    ]

    def extract(self, request: Request, request_type: RequestType):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request: Request):
        if self._CIPC_REGEX.match(request.path.decode('ascii')):
            return {'vendor': 'Cisco', 'model': 'CIPC'}
        for regex in self._FILENAME_REGEXES:
            m = regex.match(request.path.decode('ascii'))
            if m:
                dev_info = {'vendor': 'Cisco'}
                if m.lastindex == 1:
                    try:
                        dev_info['mac'] = norm_mac(m.group(1))
                    except ValueError as e:
                        logger.warning('Could not normalize MAC address: %s', e)
                return dev_info


class BaseCiscoTFTPDeviceInfoExtractor:
    _CIPC_REGEX = re.compile(r'^Communicator[/\\]')
    _FILENAME_REGEXES = [
        re.compile(r'^SEP([\dA-F]{12})\.cnf\.xml$'),
        re.compile(r'^CTLSEP([\dA-F]{12})\.tlv$'),
        re.compile(r'^ITLSEP([\dA-F]{12})\.tlv$'),
        re.compile(r'^ITLFile\.tlv$'),
    ]

    def extract(self, request: dict, request_type: RequestType):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request: dict):
        packet: dict = request['packet']
        filename = packet['filename']
        if self._CIPC_REGEX.match(filename):
            return {'vendor': 'Cisco', 'model': 'CIPC'}
        for regex in self._FILENAME_REGEXES:
            m = regex.match(filename)
            if m:
                dev_info = {'vendor': 'Cisco'}
                return dev_info

    def __repr__(self):
        return object.__repr__(self) + "-SCCP"


_ZONE_MAP = {
    'Etc/GMT+12': 'Dateline Standard Time',
    'Pacific/Samoa': 'Samoa Standard Time ',
    'US/Hawaii': 'Hawaiian Standard Time ',
    'US/Alaska': 'Alaskan Standard/Daylight Time',
    'US/Pacific': 'Pacific Standard/Daylight Time',
    'US/Mountain': 'Mountain Standard/Daylight Time',
    'Etc/GMT+7': 'US Mountain Standard Time',
    'US/Central': 'Central Standard/Daylight Time',
    'America/Mexico_City': 'Mexico Standard/Daylight Time',
    #    '': u'Canada Central Standard Time',
    #    '': u'SA Pacific Standard Time',
    'US/Eastern': 'Eastern Standard/Daylight Time',
    'Etc/GMT+5': 'US Eastern Standard Time',
    'Canada/Atlantic': 'Atlantic Standard/Daylight Time',
    'Etc/GMT+4': 'SA Western Standard Time',
    'Canada/Newfoundland': 'Newfoundland Standard/Daylight Time',
    'America/Sao_Paulo': 'South America Standard/Daylight Time',
    'Etc/GMT+3': 'SA Eastern Standard Time',
    'Etc/GMT+2': 'Mid-Atlantic Standard/Daylight Time',
    'Atlantic/Azores': 'Azores Standard/Daylight Time',
    'Europe/London': 'GMT Standard/Daylight Time',
    'Etc/GMT': 'Greenwich Standard Time',
    #    'Europe/Belfast': u'W. Europe Standard/Daylight Time',
    #    '': u'GTB Standard/Daylight Time',
    'Egypt': 'Egypt Standard/Daylight Time',
    'Europe/Athens': 'E. Europe Standard/Daylight Time',
    #    'Europe/Rome': u'Romance Standard/Daylight Time',
    'Europe/Paris': 'Central Europe Standard/Daylight Time',
    'Africa/Johannesburg': 'South Africa Standard Time ',
    'Asia/Jerusalem': 'Jerusalem Standard/Daylight Time',
    'Asia/Riyadh': 'Saudi Arabia Standard Time',
    'Europe/Moscow': 'Russian Standard/Daylight Time',  # Russia covers 8 time zones.
    'Iran': 'Iran Standard/Daylight Time',
    #    '': u'Caucasus Standard/Daylight Time',
    'Etc/GMT-4': 'Arabian Standard Time',
    'Asia/Kabul': 'Afghanistan Standard Time ',
    'Etc/GMT-5': 'West Asia Standard Time',
    #    '': u'Ekaterinburg Standard Time',
    'Asia/Calcutta': 'India Standard Time',
    'Etc/GMT-6': 'Central Asia Standard Time ',
    'Etc/GMT-7': 'SE Asia Standard Time',
    #    '': u'China Standard/Daylight Time', # China doesn't observe DST since 1991
    'Asia/Taipei': 'Taipei Standard Time',
    'Asia/Tokyo': 'Tokyo Standard Time',
    'Australia/ACT': 'Cen. Australia Standard/Daylight Time',
    'Australia/Brisbane': 'AUS Central Standard Time',
    #    '': u'E. Australia Standard Time',
    #    '': u'AUS Eastern Standard/Daylight Time',
    'Etc/GMT-10': 'West Pacific Standard Time',
    'Australia/Tasmania': 'Tasmania Standard/Daylight Time',
    'Etc/GMT-11': 'Central Pacific Standard Time',
    'Etc/GMT-12': 'Fiji Standard Time',
    #    '': u'New Zealand Standard/Daylight Time',
}


def _gen_tz_map():
    result = {}
    for tz_name, param_value in _ZONE_MAP.items():
        tzinfo = tzinform.get_timezone_info(tz_name)
        inner_dict = result.setdefault(tzinfo['utcoffset'].as_minutes, {})
        if not tzinfo['dst']:
            inner_dict[None] = param_value
        else:
            inner_dict[tzinfo['dst']['as_string']] = param_value
    return result


class BaseCiscoSccpPlugin(StandardPlugin):
    # XXX actually, we didn't find which encoding Cisco SCCP are using
    _ENCODING = 'UTF-8'
    _TZ_MAP = _gen_tz_map()
    _TZ_VALUE_DEF = 'Eastern Standard/Daylight Time'
    _LOCALE = {
        # <locale>: (<name>, <lang code>, <network locale>)
        'de_DE': ('german_germany', 'de', 'germany'),
        'en_US': ('english_united_states', 'en', 'united_states'),
        'es_ES': ('spanish_spain', 'es', 'spain'),
        'fr_FR': ('french_france', 'fr', 'france'),
        'fr_CA': ('french_france', 'fr', 'canada'),
    }
    _SENSITIVE_FILENAME_REGEX = re.compile(r'^SEP[0-9A-F]{12}\.cnf\.xml$')

    def __init__(self, app, plugin_dir, gen_cfg, spec_cfg):
        super().__init__(app, plugin_dir, gen_cfg, spec_cfg)

        self._tpl_helper = TemplatePluginHelper(plugin_dir)

        downloaders = FetchfwPluginHelper.new_downloaders(gen_cfg.get('proxies'))
        fetchfw_helper = FetchfwPluginHelper(plugin_dir, downloaders)

        self.services = fetchfw_helper.services()

        # Maybe find a way to bind to a specific port
        # without changing the general http_port setting of wazo-provd ?
        # At the moment, http_port 6970 must be set in /etc/xivo/provd/provd.conf
        self.http_service = HTTPNoListingFileService(self._tftpboot_dir)

        self.tftp_service = TFTPFileService(self._tftpboot_dir)

    dhcp_dev_info_extractor = BaseCiscoDHCPDeviceInfoExtractor()
    http_dev_info_extractor = BaseCiscoHTTPDeviceInfoExtractor()
    tftp_dev_info_extractor = BaseCiscoTFTPDeviceInfoExtractor()

    def _add_locale(self, raw_config):
        locale = raw_config.get('locale')
        if locale in self._LOCALE:
            raw_config['XX_locale'] = self._LOCALE[locale]

    def _tzinfo_to_value(self, tzinfo):
        utcoffset_m = tzinfo['utcoffset'].as_minutes
        if utcoffset_m not in self._TZ_MAP:
            # No UTC offset matching. Let's try finding one relatively close...
            for supp_offset in [30, -30, 60, -60]:
                if utcoffset_m + supp_offset in self._TZ_MAP:
                    utcoffset_m += supp_offset
                    break
            else:
                return self._TZ_VALUE_DEF

        dst_map = self._TZ_MAP[utcoffset_m]
        if tzinfo['dst']:
            dst_key = tzinfo['dst']['as_string']
        else:
            dst_key = None
        if dst_key not in dst_map:
            # No DST rules matching. Fallback on all-standard time or random
            # DST rule in last resort...
            if None in dst_map:
                dst_key = None
            else:
                dst_key = list(dst_map)[0]
        return dst_map[dst_key]

    def _add_timezone(self, raw_config):
        raw_config['XX_timezone'] = self._TZ_VALUE_DEF
        if 'timezone' in raw_config:
            try:
                tzinfo = tzinform.get_timezone_info(raw_config['timezone'])
            except tzinform.TimezoneNotFoundError as e:
                logger.info('Unknown timezone: %s', e)
            else:
                raw_config['XX_timezone'] = self._tzinfo_to_value(tzinfo)

    def _add_xivo_phonebook_url(self, raw_config):
        plugins.add_xivo_phonebook_url(raw_config, 'cisco', entry_point='menu')

    def _update_call_managers(self, raw_config):
        for priority, call_manager in raw_config['sccp_call_managers'].items():
            call_manager['XX_priority'] = str(int(priority) - 1)

    def _dev_specific_filename(self, device: Dict[str, str]) -> str:
        # Return the device specific filename (not pathname) of device
        formatted_mac = format_mac(device['mac'], separator='', uppercase=True)
        return f'SEP{formatted_mac}.cnf.xml'

    def _check_config(self, raw_config):
        if 'tftp_port' not in raw_config:
            raise RawConfigError('only support configuration via TFTP')

    def _check_device(self, device):
        if 'mac' not in device:
            raise Exception('MAC address needed for device configuration')

    def configure(self, device, raw_config):
        self._check_config(raw_config)
        self._check_device(device)
        filename = self._dev_specific_filename(device)
        tpl = self._tpl_helper.get_dev_template(filename, device)

        # TODO check support for addons, and test what the addOnModules is
        #      really doing...
        raw_config['XX_addons'] = ''
        self._add_locale(raw_config)
        self._add_timezone(raw_config)
        self._add_xivo_phonebook_url(raw_config)
        self._update_call_managers(raw_config)

        path = os.path.join(self._tftpboot_dir, filename)
        self._tpl_helper.dump(tpl, raw_config, path, self._ENCODING)

    def deconfigure(self, device):
        path = os.path.join(self._tftpboot_dir, self._dev_specific_filename(device))
        try:
            os.remove(path)
        except OSError as e:
            # ignore
            logger.info('error while removing file: %s', e)

    def synchronize(self, device, raw_config):
        return defer.fail(Exception('operation not supported'))

    def is_sensitive_filename(self, filename):
        return bool(self._SENSITIVE_FILENAME_REGEX.match(filename))
