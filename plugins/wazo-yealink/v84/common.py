# Copyright 2011-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import logging
import re
import os.path
from typing import Dict, Optional

from provd import plugins
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

logger = logging.getLogger('plugin.xivo-yealink')


class BaseYealinkHTTPDeviceInfoExtractor:
    _UA_REGEX_LIST = [
        re.compile(r'^[yY]ealink\s+SIP(?: VP)?-(\w+)\s+([\d.]+)\s+([\da-fA-F:]{17})$'),
        re.compile(r'^[yY]ealink\s+(CP860|W52P|W60B)\s+([\d.]+)\s+([\da-fA-F:]{17})$'),
        re.compile(r'(VP530P?|W52P|W60B)\s+([\d.]+)\s+([\da-fA-F:]{17})$'),
        re.compile(r'[yY]ealink-(\w+)\s+([\d.]+)\s+([\d.]+)$'),
    ]

    def extract(self, request: Request, request_type: RequestType):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request: Request):
        ua = request.getHeader(b'User-Agent')
        if ua:
            return self._extract_from_ua(ua.decode('ascii'))
        return self._extract_from_path(request)

    def _extract_from_ua(self, ua: str):
        # HTTP User-Agent:
        #   "Yealink CP860 37.72.0.5 00:15:65:8a:37:86"
        #   "yealink SIP-T18 18.0.0.80 00:15:65:27:3e:05"
        #   "Yealink SIP-T19P_E2 53.80.0.3 00:15:65:4c:4c:26"
        #   "Yealink SIP-T20P 9.72.0.30 00:15:65:5e:16:7c"
        #   "Yealink SIP-T21P 34.72.0.1 00:15:65:4c:4c:26"
        #   "Yealink SIP-T21P_E2 52.80.0.3 00:15:65:4c:4c:26"
        #   "Yealink SIP-T22P 7.72.0.30 00:15:65:39:31:fc"
        #   "Yealink SIP-T23G 44.80.0.60 00:15:65:93:70:f2"
        #   "Yealink SIP-T26P 6.72.0.30 00:15:65:4b:57:d2"
        #   "Yealink SIP-T27P 45.80.0.25 00:15:65:8c:48:12"
        #   "yealink SIP-T28P 2.70.0.140 00:15:65:13:ae:0b"
        #   "Yealink SIP-T38G  38.70.0.125 00:15:65:2f:c3:5e"
        #   "Yealink SIP-T40P 54.80.0.10 00:15:65:94:86:64"
        #   "Yealink SIP-T41P 36.72.0.1 00:15:65:53:83:22"
        #   "Yealink SIP-T42G 29.72.0.1 00:15:65:4c:3b:b0"
        #   "Yealink SIP-T46G 28.72.0.1 00:15:65:4a:a9:37"
        #   "Yealink SIP-T48G 35.72.0.6 00:15:65:5c:60:82"
        #   "Yealink SIP VP-T49G 51.80.0.10 00:15:65:9b:5a:44"
        #   "Yealink SIP-W52P 25.73.0.20 00:15:65:40:ae:35"
        #   "W52P 25.30.0.2 00:15:65:44:b3:7c"
        #   "Yealink W52P 25.80.0.15 00:15:65:b8:60:05"
        #   "Yealink W60B 77.81.0.35 80:5e:c0:09:ab:dc"
        #   "Yealink-T46G 28.71.0.81 28.1.0.128.0.0.0"
        #   "VP530P 23.70.0.40 00:15:65:31:4b:c0"
        #   "VP530 23.70.0.41 00:15:65:3d:58:e3"

        for UA_REGEX in self._UA_REGEX_LIST:
            m = UA_REGEX.match(ua)
            if m:
                model, version, raw_mac = m.groups()
                device_info = {
                    'vendor': 'Yealink',
                    'model': model,
                    'version': version,
                }
                try:
                    device_info['mac'] = norm_mac(raw_mac.decode('ascii'))
                except ValueError as e:
                    logger.warning(
                        'Could not normalize MAC address "%s": %s', raw_mac, e
                    )
                return device_info
        return None

    def _extract_from_path(self, request: Request):
        if request.path.startswith(b'/001565'):
            raw_mac = request.path[1:-4]
            try:
                return {'mac': norm_mac(raw_mac.decode('ascii'))}
            except ValueError as e:
                logger.warning('Could not normalize MAC address "%s": %s', raw_mac, e)
        return None


class BaseYealinkPgAssociator(BasePgAssociator):
    def __init__(self, model_versions):
        # model_versions is a dictionary which keys are model IDs and values
        # are version IDs.
        super().__init__()
        self._model_versions = model_versions

    def _do_associate(
        self, vendor: str, model: Optional[str], version: Optional[str]
    ) -> DeviceSupport:
        if vendor == 'Yealink':
            if model in self._model_versions:
                if version == self._model_versions[model]:
                    return DeviceSupport.EXACT
                return DeviceSupport.COMPLETE
            return DeviceSupport.PROBABLE
        return DeviceSupport.IMPROBABLE


class BaseYealinkFunckeyGenerator:
    def __init__(self, device, raw_config):
        self._model = device.get('model')
        self._exten_pickup_call = raw_config.get('exten_pickup_call')
        self._funckeys = raw_config['funckeys']
        self._sip_lines = raw_config['sip_lines']
        self._lines = []

    def generate(self):
        prefixes = BaseYealinkFunckeyPrefixIterator(self._model)
        for funckey_no, prefix in enumerate(prefixes, start=1):
            funckey = self._funckeys.get(str(funckey_no))
            self._format_funckey(prefix, funckey_no, funckey)
            self._lines.append('')

        return '\n'.join(self._lines)

    def _format_funckey(self, prefix, funckey_no, funckey):
        if funckey is None:
            if str(funckey_no) in self._sip_lines:
                self._format_funckey_line(prefix, str(funckey_no))
            else:
                self._format_funckey_null(prefix)
            return

        funckey_type = funckey['type']
        if funckey_type == 'speeddial':
            self._format_funckey_speeddial(prefix, funckey)
        elif funckey_type == 'blf':
            self._format_funckey_blf(prefix, funckey)
        elif funckey_type == 'park':
            self._format_funckey_park(prefix, funckey)
        else:
            logger.info('Unsupported funckey type: %s', funckey_type)

    def _format_funckey_null(self, prefix):
        self._lines += [
            f'{prefix}.type = 0',
            f'{prefix}.line = %NULL%',
            f'{prefix}.value = %NULL%',
            f'{prefix}.label = %NULL%',
        ]

    def _format_funckey_speeddial(self, prefix, funckey):
        self._lines += [
            f'{prefix}.type = 13',
            f'{prefix}.line = {funckey.get("line", 1)}',
            f'{prefix}.value = {funckey["value"]}',
            f'{prefix}.label = {funckey.get("label", "")}',
        ]

    def _format_funckey_park(self, prefix, funckey):
        self._lines += [
            f'{prefix}.type = 10',
            f'{prefix}.line = {funckey.get("line", 1)}',
            f'{prefix}.value = {funckey["value"]}',
            f'{prefix}.label = {funckey.get("label", "")}',
        ]

    def _format_funckey_blf(self, prefix, funckey):
        line_no = funckey.get('line', 1)
        if self._model in ('T32G', 'T38G'):
            line_no -= 1
        self._lines.append(f'{prefix}.type = 16')
        self._lines.append(f'{prefix}.line = {line_no}')
        self._lines.append(f'{prefix}.value = {funckey["value"]}')
        self._lines.append(f'{prefix}.label = {funckey.get("label", "")}')
        if self._exten_pickup_call:
            self._lines.append(f'{prefix}.extension = {self._exten_pickup_call}')

    def _format_funckey_line(self, prefix, line):
        self._lines += [
            f'{prefix}.type = 15',
            f'{prefix}.line = {line}',
            f'{prefix}.value = {self._sip_lines[line]["number"]}',
            f'{prefix}.label = {self._sip_lines[line]["number"]}',
        ]


class BaseYealinkFunckeyPrefixIterator:

    _NB_LINEKEY = {
        'CP920': 0,
        'CP960': 0,
        'T19P_E2': 0,
        'T21P_E2': 2,
        'T23P': 3,
        'T23G': 3,
        'T27G': 21,
        'T40G': 3,
        'T40P': 3,
        'T41S': 15,
        'T42S': 15,
        'T46S': 27,
        'T48S': 29,
        'T52S': 21,
        'T53': 21,
        'T53W': 21,
        'T54S': 27,
        'T54W': 27,
        'T57W': 29,
        'T58': 27,
    }
    _NB_MEMORYKEY = {
        'CP920': 0,
        'CP960': 0,
        'T19P_E2': 0,
        'T21P_E2': 0,
        'T23P': 0,
        'T23G': 0,
        'T27G': 0,
        'T40G': 0,
        'T40P': 0,
        'T41S': 0,
        'T42S': 0,
        'T46S': 0,
        'T48S': 0,
        'T52S': 0,
        'T53': 0,
        'T53W': 0,
        'T54S': 0,
        'T54W': 0,
        'T57W': 0,
        'T58': 0,
    }

    class NullExpansionModule:
        key_count = 0
        max_daisy_chain = 0

    class EXP40ExpansionModule(NullExpansionModule):
        key_count = 40
        max_daisy_chain = 6

    class EXP50ExpansionModule(NullExpansionModule):
        key_count = 60
        max_daisy_chain = 3

    def __init__(self, model):
        self._nb_linekey = self._nb_linekey_by_model(model)
        self._nb_memorykey = self._nb_memorykey_by_model(model)
        self._expmod = self._expmod_by_model(model)

    def _nb_linekey_by_model(self, model):
        if model is None:
            logger.info('No model information; no linekey will be configured')
            return 0
        nb_linekey = self._NB_LINEKEY.get(model)
        if nb_linekey is None:
            logger.info('Unknown model %s; no linekey will be configured', model)
            return 0
        return nb_linekey

    def _nb_memorykey_by_model(self, model):
        if model is None:
            logger.info('No model information; no memorykey will be configured')
            return 0
        nb_memorykey = self._NB_MEMORYKEY.get(model)
        if nb_memorykey is None:
            logger.info('Unknown model %s; no memorykey will be configured', model)
            return 0
        return nb_memorykey

    def _expmod_by_model(self, model):
        if model in ('T27G', 'T46S', 'T48S'):
            return self.EXP40ExpansionModule
        elif model.startswith('T5'):
            return self.EXP50ExpansionModule
        else:
            return self.NullExpansionModule

    def __iter__(self):
        for linekey_no in range(1, self._nb_linekey + 1):
            yield f'linekey.{linekey_no}'
        for memorykey_no in range(1, self._nb_memorykey + 1):
            yield f'memorykey.{memorykey_no}'
        for expmod_no in range(1, self._expmod.max_daisy_chain + 1):
            for expmodkey_no in range(1, self._expmod.key_count + 1):
                yield f'expansion_module.{expmod_no}.key.{expmodkey_no}'


class BaseYealinkPlugin(StandardPlugin):
    _ENCODING = 'UTF-8'
    _LOCALE = {
        'de_DE': ('German', 'Germany', '2'),
        'en_US': ('English', 'United States', '0'),
        'es_ES': ('Spanish', 'Spain', '6'),
        'fr_FR': ('French', 'France', '1'),
        'fr_CA': ('French', 'United States', '1'),
    }
    _SIP_DTMF_MODE = {
        'RTP-in-band': '0',
        'RTP-out-of-band': '1',
        'SIP-INFO': '2',
    }
    _SIP_TRANSPORT = {
        'udp': '0',
        'tcp': '1',
        'tls': '2',
    }
    _SIP_TRANSPORT_DEF = '0'
    _NB_SIP_ACCOUNTS = {
        'CP920': 1,
        'CP960': 1,
        'T19P_E2': 1,
        'T21P_E2': 2,
        'T23P': 3,
        'T23G': 3,
        'T27G': 6,
        'T40G': 3,
        'T40P': 3,
        'T41S': 6,
        'T42S': 12,
        'T46S': 16,
        'T48S': 16,
        'T52S': 12,
        'T53': 12,
        'T53W': 12,
        'T54S': 16,
        'T54W': 16,
        'T57W': 16,
        'T58': 16,
    }
    _SENSITIVE_FILENAME_REGEX = re.compile(r'^[0-9a-f]{12}\.cfg')

    def __init__(self, app, plugin_dir, gen_cfg, spec_cfg):
        super().__init__(app, plugin_dir, gen_cfg, spec_cfg)

        self._tpl_helper = TemplatePluginHelper(plugin_dir)

        downloaders = FetchfwPluginHelper.new_downloaders(gen_cfg.get('proxies'))
        fetchfw_helper = FetchfwPluginHelper(plugin_dir, downloaders)

        self.services = fetchfw_helper.services()
        self.http_service = HTTPNoListingFileService(self._tftpboot_dir)

    http_dev_info_extractor = BaseYealinkHTTPDeviceInfoExtractor()

    def configure_common(self, raw_config):
        for filename, fw_filename, tpl_filename in self._COMMON_FILES:
            tpl = self._tpl_helper.get_template(f'common/{tpl_filename}')
            dst = os.path.join(self._tftpboot_dir, filename)
            raw_config['XX_fw_filename'] = fw_filename
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

    def _add_fkeys(self, device, raw_config):
        funckey_generator = BaseYealinkFunckeyGenerator(device, raw_config)
        raw_config['XX_fkeys'] = funckey_generator.generate()

    def _add_country_and_lang(self, raw_config):
        locale = raw_config.get('locale')
        if locale in self._LOCALE:
            (
                raw_config['XX_lang'],
                raw_config['XX_country'],
                raw_config['XX_handset_lang'],
            ) = self._LOCALE[locale]

    def _format_dst_change(self, dst_change):
        day, month, time = dst_change['day'], dst_change['month'], dst_change['time']
        if day.startswith('D'):
            return f'{month:02d}/{int(day[1:]):02d}/{time.as_hours:02d}'
        else:
            week, weekday = list(map(int, day[1:].split('.')))
            weekday = tzinform.week_start_on_monday(weekday)
            return f'{month:d}/{week:d}/{weekday:d}/{time.as_hours:d}'

    def _format_tz_info(self, tzinfo):
        lines = [
            f'local_time.time_zone = {min(max(tzinfo["utcoffset"].as_hours, -11), 12):+d}'
        ]
        if tzinfo['dst'] is None:
            lines.append('local_time.summer_time = 0')
        else:
            lines.append('local_time.summer_time = 1')
            if tzinfo['dst']['start']['day'].startswith('D'):
                lines.append('local_time.dst_time_type = 0')
            else:
                lines.append('local_time.dst_time_type = 1')
            lines.append(
                f'local_time.start_time = {self._format_dst_change(tzinfo["dst"]["start"])}'
            )
            lines.append(
                f'local_time.end_time = {self._format_dst_change(tzinfo["dst"]["end"])}'
            )
            lines.append(f'local_time.offset_time = {tzinfo["dst"]["save"].as_minutes}')
        return '\n'.join(lines)

    def _add_timezone(self, raw_config):
        if 'timezone' in raw_config:
            try:
                tzinfo = tzinform.get_timezone_info(raw_config['timezone'])
            except tzinform.TimezoneNotFoundError as e:
                logger.warning('Unknown timezone: %s', e)
            else:
                raw_config['XX_timezone'] = self._format_tz_info(tzinfo)

    def _add_sip_transport(self, raw_config):
        raw_config['XX_sip_transport'] = self._SIP_TRANSPORT.get(
            raw_config.get('sip_transport'), self._SIP_TRANSPORT_DEF
        )

    def _add_xx_sip_lines(self, device, raw_config):
        sip_lines = raw_config['sip_lines']
        sip_accounts = self._get_sip_accounts(device.get('model'))
        if not sip_accounts:
            xx_sip_lines = dict(sip_lines)
        else:
            xx_sip_lines = {}
            for line_no in range(1, sip_accounts + 1):
                line_no = str(line_no)
                xx_sip_lines[line_no] = sip_lines.get(line_no)
        raw_config['XX_sip_lines'] = xx_sip_lines

    def _get_sip_accounts(self, model):
        return self._NB_SIP_ACCOUNTS.get(model)

    def _add_xivo_phonebook_url(self, raw_config):
        plugins.add_xivo_phonebook_url(
            raw_config, 'yealink', entry_point='lookup', qs_suffix='term=#SEARCH'
        )

    def _add_wazo_phoned_user_service_url(self, raw_config, service):
        if hasattr(plugins, 'add_wazo_phoned_user_service_url'):
            plugins.add_wazo_phoned_user_service_url(raw_config, 'yealink', service)

    def _dev_specific_filename(self, device: Dict[str, str]) -> str:
        # Return the device specific filename (not pathname) of device
        formatted_mac = format_mac(device['mac'], separator='')
        return f'{formatted_mac}.cfg'

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
        self._add_xx_sip_lines(device, raw_config)
        self._add_xivo_phonebook_url(raw_config)
        self._add_wazo_phoned_user_service_url(raw_config, 'dnd')
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
