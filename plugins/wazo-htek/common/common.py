# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import logging
import re
import os.path

from provd import plugins
from provd import tzinform
from provd import synchronize
from provd.devices.config import RawConfigError
from provd.devices.pgasso import BasePgAssociator, DeviceSupport
from provd.plugins import StandardPlugin, FetchfwPluginHelper, TemplatePluginHelper
from provd.servers.http import HTTPNoListingFileService
from provd.servers.http_site import Request
from provd.devices.ident import RequestType
from provd.util import norm_mac, format_mac
from twisted.internet import defer

logger = logging.getLogger('plugin.wazo-htek')


class BaseHtekHTTPDeviceInfoExtractor:
    _UA_REGEX_LIST = [re.compile(r'^Htek ([^ ]+) ([^ ]+) ([^ ]+)$')]

    def extract(self, request: Request, request_type: RequestType):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request: Request):
        ua = request.getHeader(b'User-Agent')
        if ua:
            return self._extract_from_ua(ua.decode('ascii'))

    def _extract_from_ua(self, ua: str):
        # HTTP User-Agent:
        #   "Htek UC903 2.0.4.2 00:1f:c1:1c:22:a9"

        for UA_REGEX in self._UA_REGEX_LIST:
            m = UA_REGEX.match(ua)
            if m:
                raw_model, raw_version, raw_mac = m.groups()
                device_info = {
                    'vendor': 'Htek',
                    'model': raw_model,
                    'version': raw_version,
                }
                try:
                    device_info['mac'] = norm_mac(raw_mac)
                except ValueError as e:
                    logger.warning(
                        'Could not normalize MAC address "%s": %s', raw_mac, e
                    )
                return device_info
        return None


class BaseHtekPgAssociator(BasePgAssociator):
    def __init__(self, model_versions):
        # model_versions is a dictionary which keys are model IDs and values
        # are version IDs.
        super().__init__()
        self._model_versions = model_versions

    def _do_associate(
        self, vendor: str, model: str | None, version: str | None
    ) -> DeviceSupport:
        if vendor == 'Htek':
            if model in self._model_versions:
                if version == self._model_versions[model]:
                    return DeviceSupport.EXACT
                return DeviceSupport.COMPLETE
            return DeviceSupport.PROBABLE
        return DeviceSupport.IMPROBABLE


class BaseHtekPlugin(StandardPlugin):
    _ENCODING = 'UTF-8'
    _LOCALE = {
        'de_DE': ('German', 'Germany'),
        'en_US': ('English', 'United States'),
        'en_GB': ('English', 'Great Britain'),
        'es_ES': ('Spanish', 'Spain'),
        'fr_FR': ('French', 'France'),
        'fr_CA': ('French', 'United States'),
    }

    # Used for tone select
    _COUNTRIES = {
        'Custom': 0,
        'Australia': 1,
        'Austria': 2,
        'Brazil': 3,
        'Belgium': 4,
        'China': 5,
        'Chile': 6,
        'Czech': 7,
        'Denmark': 8,
        'Finland': 9,
        'France': 10,
        'Germany': 11,
        'Great Britain': 12,
        'Greece': 13,
        'Hungary': 14,
        'Lithuania': 15,
        'India': 16,
        'Italy': 17,
        'Japan': 18,
        'Mexico': 19,
        'New Zealand': 20,
        'Netherlands': 21,
        'Norway': 22,
        'Portugal': 23,
        'Spain': 24,
        'Switzerland': 25,
        'Sweden': 26,
        'Russia': 27,
        'United States': 28,
    }

    _SIP_DTMF_MODE = {
        'RTP-out-of-band': '0',
        'RTP-in-band': '1',
        'SIP-INFO': '2',
    }
    _SIP_TRANSPORT = {
        'udp': '0',
        'tcp': '1',
        'tls': '2',
    }
    _SIP_TRANSPORT_DEF = '0'
    _NB_LINEKEYS = {
        'UC926': 36,
        'UC926E': 36,
        'UC924': 28,
        'UC924E': 28,
        'UC923': 20,
        'UC912': 12,
        'UC912E': 12,
        'UC912G': 12,
        'UC903': 20,
        'UC862': 14,
        'UC860': 14,
        'UC860P': 14,
        'UC842': 4,
        'UC840': 4,
        'UC840P': 4,
        'UC806': 4,
        'UC806T': 4,
        'UC804': 4,
        'UC804T': 4,
        'UC803': 0,
        'UC803T': 0,
        'UC802': 0,
        'UC802T': 0,
    }

    _TZ_INFO = {
        (-11, 00): 105,
        (-10, 00): 2,
        (-9, 00): 3,
        (-8, 00): 6,
        (-7, 00): 10,
        (-6, 00): 14,
        (-5, 00): 18,
        (-4, 30): 19,
        (-4, 00): 20,
        (-3, 30): 26,
        (-3, 00): 30,
        (-2, 00): 31,
        (-1, 00): 32,
        (00, 00): 33,
        (1, 00): 49,
        (2, 00): 57,
        (3, 00): 73,
        (3, 30): 74,
        (4, 00): 77,
        (5, 00): 83,
        (5, 30): 84,
        (6, 00): 85,
        (7, 00): 88,
        (8, 00): 89,
        (9, 00): 93,
        (9, 30): 94,
        (10, 00): 96,
        (10, 30): 100,
        (11, 00): 101,
        (12, 00): 102,
        (12, 45): 103,
        (13, 00): 104,
    }
    _SENSITIVE_FILENAME_REGEX = re.compile(r'^cfg[0-9a-f]{12}\.xml')

    def __init__(self, app, plugin_dir, gen_cfg, spec_cfg):
        super().__init__(app, plugin_dir, gen_cfg, spec_cfg)

        self._tpl_helper = TemplatePluginHelper(plugin_dir)

        downloaders = FetchfwPluginHelper.new_downloaders(gen_cfg.get('proxies'))
        fetchfw_helper = FetchfwPluginHelper(plugin_dir, downloaders)

        self.services = fetchfw_helper.services()
        self.http_service = HTTPNoListingFileService(self._tftpboot_dir)

    http_dev_info_extractor = BaseHtekHTTPDeviceInfoExtractor()

    def configure_common(self, raw_config):
        for filename, tpl_filename in self._COMMON_FILES:
            tpl = self._tpl_helper.get_template(f'common/{tpl_filename}')
            dst = os.path.join(self._tftpboot_dir, filename)
            self._tpl_helper.dump(tpl, raw_config, dst, self._ENCODING)

    def _update_sip_lines(self, raw_config):
        for line_no, line in raw_config['sip_lines'].items():
            # set line number
            line['XX_line_no'] = int(line_no)
            # set dtmf inband transfer
            dtmf_mode = line.get('dtmf_mode') or raw_config.get('sip_dtmf_mode')
            if dtmf_mode in self._SIP_DTMF_MODE:
                line['XX_dtmf_type'] = self._SIP_DTMF_MODE[dtmf_mode]
            # set voicemail
            if 'voicemail' not in line and 'exten_voicemail' in raw_config:
                line['voicemail'] = raw_config['exten_voicemail']
            # set proxy_ip
            if 'proxy_ip' not in line:
                line['proxy_ip'] = raw_config['sip_proxy_ip']
            # set proxy_port
            if 'proxy_port' not in line and 'sip_proxy_port' in raw_config:
                line['proxy_port'] = raw_config['sip_proxy_port']

    def _gen_param_num(self, line, offset=0):
        '''Method that generates line parameter numbers for the config file

        There are several steps in the numbering of parameters that need to
        be supported.'''
        param_nb = 0
        mode_nb = 0
        limit_step1 = 5
        limit_step2 = 37
        mode_base = 20600
        param_step1_base = 41200
        param_step2_base = 20200
        param_step3_base = 23000
        line = int(line)
        if line < limit_step1:
            param_nb = param_step1_base + line - 1 + 100 * offset
            mode_nb = mode_base + line - 1
        elif line >= limit_step1 and line < limit_step2:
            param_nb = param_step2_base + offset + 5 * (line - limit_step1)
            mode_nb = mode_base + line - 1
        else:
            param_nb = param_step3_base + offset + 5 * (line - limit_step2)
            mode_nb = param_nb
        return param_nb, mode_nb

    def _add_fkeys(self, device, raw_config):
        # Setting up the line/function keys
        complete_fkeys = {}
        fkeys = raw_config['funckeys']
        fkey_type_assoc = {'': 0, 'speeddial': 2, 'blf': 3, 'park': 8}

        if (
            'model' in device
            and device['model'] is not None
            and device['model'] in self._NB_LINEKEYS
        ):
            for key_nb in range(1, self._NB_LINEKEYS[device['model']] + 1):
                if str(key_nb) in raw_config['sip_lines']:
                    sip_line = raw_config['sip_lines'][str(key_nb)]
                    val = {'type': 1, 'value': '', 'label': sip_line['number']}
                else:
                    val = fkeys.get(str(key_nb), {'type': '', 'value': '', 'label': ''})
                    val['type'] = fkey_type_assoc[val['type']]
                complete_fkeys[key_nb] = {
                    'type': {
                        'p_nb': self._gen_param_num(key_nb)[0],
                        'val': val['type'],
                    },
                    'mode': {'p_nb': self._gen_param_num(key_nb)[1]},
                    'value': {
                        'p_nb': self._gen_param_num(key_nb, offset=1)[0],
                        'val': val['value'],
                    },
                    'label': {
                        'p_nb': self._gen_param_num(key_nb, offset=2)[0],
                        'val': val['label'],
                    },
                    'account': {'p_nb': self._gen_param_num(key_nb, offset=3)[0]},
                    'extension': {
                        'p_nb': self._gen_param_num(key_nb, offset=4)[0],
                        'val': val['value'],
                    },
                }
            raw_config['XX_fkeys'] = complete_fkeys

    def _add_country_and_lang(self, raw_config):
        locale = raw_config.get('locale')
        if locale in self._LOCALE:
            (lang, country) = self._LOCALE[locale]
            (raw_config['XX_lang'], raw_config['XX_country']) = (
                lang,
                self._COUNTRIES[country],
            )

    def _add_timezone(self, raw_config):
        timezone = raw_config.get('timezone', 'Etc/UTC')
        tz_db = tzinform.TextTimezoneInfoDB()
        tz_timezone_info = tz_db.get_timezone_info(timezone)
        tz_info = tz_timezone_info['utcoffset'].as_hms
        offset_hour = tz_info[0]
        offset_minutes = tz_info[1]

        if (offset_hour, offset_minutes) in self._TZ_INFO:
            raw_config['XX_timezone_code'] = self._TZ_INFO[
                (offset_hour, offset_minutes)
            ]
        else:
            raw_config['XX_timezone_code'] = self._TZ_INFO[(-5, 0)]

    def _add_sip_transport(self, raw_config):
        raw_config['XX_sip_transport'] = self._SIP_TRANSPORT.get(
            raw_config.get('sip_transport'), self._SIP_TRANSPORT_DEF
        )

    def _add_xivo_phonebook_url(self, raw_config):
        plugins.add_xivo_phonebook_url(raw_config, 'htek', entry_point='lookup')

    def _dev_specific_filename(self, device: dict[str, str]) -> str:
        # Return the device specific filename (not pathname) of device
        formatted_mac = format_mac(device['mac'], separator='')
        return f'cfg{formatted_mac}.xml'

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

        self._add_fkeys(device, raw_config)
        self._add_country_and_lang(raw_config)
        self._add_timezone(raw_config)
        self._add_sip_transport(raw_config)
        self._update_sip_lines(raw_config)
        self._add_xivo_phonebook_url(raw_config)
        raw_config['XX_options'] = device.get('options', {})

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
        return synchronize.standard_sip_synchronize(device)

    def get_remote_state_trigger_filename(self, device):
        if 'mac' not in device:
            return None

        return self._dev_specific_filename(device)

    def is_sensitive_filename(self, filename):
        return bool(self._SENSITIVE_FILENAME_REGEX.match(filename))
