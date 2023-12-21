# Copyright 2022-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import logging
import os.path
import re
from typing import Any

from provd import plugins, synchronize, tzinform
from provd.devices.config import RawConfigError
from provd.devices.ident import RequestType
from provd.devices.pgasso import BasePgAssociator, DeviceSupport
from provd.plugins import FetchfwPluginHelper, StandardPlugin, TemplatePluginHelper
from provd.servers.http import HTTPNoListingFileService
from provd.servers.http_site import Request
from provd.util import format_mac, norm_mac
from twisted.internet import defer

logger = logging.getLogger('plugin.wazo-alcatel')


class BaseAlcatelMyriadHTTPDeviceInfoExtractor:
    _UA_REGEX_MAC = re.compile(
        r'^ALE (?P<model>8028s-GE) (?P<version>([0-9]{1,4}\.?){4,5}) (?P<mac>[0-9a-f]{12})'
    )

    def extract(self, request: Request, request_type: RequestType):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request: Request):
        device_info = {}
        ua = request.getHeader(b'User-Agent')
        raw_mac = request.args.get(b'mac', [None])[0]
        if raw_mac:
            logger.debug('Got MAC from URL: "%s"', raw_mac)
            device_info['mac'] = norm_mac(raw_mac.decode('ascii'))
        if ua:
            info_from_ua = self._extract_from_ua(ua.decode('ascii'))
            if info_from_ua:
                device_info.update(info_from_ua)
        return device_info

    def _extract_from_ua(self, ua: str):
        # HTTP User-Agent:
        #   "ALE 8028s-GE 1.51.52.2204 487a55023075"
        m = self._UA_REGEX_MAC.search(ua)
        if m:
            device_info = m.groupdict()
            return {
                'vendor': 'Alcatel-Lucent',
                'model': device_info['model'],
                'mac': norm_mac(device_info['mac']),
                'version': device_info['version'],
            }


class BaseAlcatelMyriadPgAssociator(BasePgAssociator):
    def __init__(self, models_versions):
        self._models_versions = models_versions

    def _do_associate(
        self, vendor: str, model: str | None, version: str | None
    ) -> DeviceSupport:
        if vendor == 'Alcatel-Lucent':
            if model in self._models_versions:
                if version == self._models_versions.get(model, None):
                    return DeviceSupport.EXACT
                return DeviceSupport.COMPLETE
            return DeviceSupport.PROBABLE
        return DeviceSupport.IMPROBABLE


class BaseAlcatelPlugin(StandardPlugin):
    _ENCODING = 'UTF-8'

    _SIP_DTMF_MODE = {
        'off': 0,
        'RTP-in-band': 1,
        'RTP-out-of-band': 2,
        'SIP-INFO': 4,
    }

    _NB_FUNCKEYS = {
        '8028s-GE': 6,
    }
    _FUNCKEY_TYPE = {
        'blf': 59,
        'speeddial': 1,
    }
    _LANG = {
        'en': 0,
        'fr': 1,
        'de': 2,
        'it': 3,
        'es': 4,
        'nl': 5,
        'pt': 6,
        'hu': 7,
        'cs': 8,
        'sk': 9,
        'sl': 10,
        'et': 11,
        'pl': 12,
        'lt': 13,
        'lv': 14,
        'tr': 15,
        'el': 16,
        'sv': 17,
        'no': 18,
        'da': 19,
        'fi': 20,
        'is': 21,
        'zh': 22,
    }

    _SENSITIVE_FILENAME_REGEX = re.compile(r'^config\.[0-9a-f]{12}\.xml')
    http_dev_info_extractor = BaseAlcatelMyriadHTTPDeviceInfoExtractor()

    def __init__(self, app, plugin_dir, gen_cfg, spec_cfg):
        super().__init__(app, plugin_dir, gen_cfg, spec_cfg)

        self._tpl_helper = TemplatePluginHelper(plugin_dir)

        downloaders = FetchfwPluginHelper.new_downloaders(gen_cfg.get('proxies'))
        fetchfw_helper = FetchfwPluginHelper(plugin_dir, downloaders)

        self.services = fetchfw_helper.services()
        self.http_service = HTTPNoListingFileService(self._tftpboot_dir)

    def _common_templates(self):
        for tpl_format, file_format in [
            ('common/config.model.xml.tpl', 'config.{}.xml')
        ]:
            for model in self._MODELS_VERSIONS:
                yield tpl_format.format(model), file_format.format(model)

    def configure_common(self, raw_config):
        self._add_server_url(raw_config)
        for tpl_filename, filename in self._common_templates():
            tpl = self._tpl_helper.get_template(tpl_filename)
            dest_file = os.path.join(self._tftpboot_dir, filename)
            self._tpl_helper.dump(tpl, raw_config, dest_file, self._ENCODING)

    def _update_sip_lines(self, raw_config):
        proxy_ip = raw_config.get('sip_proxy_ip')
        proxy_port = raw_config.get('sip_proxy_port')
        backup_proxy_ip = raw_config.get('sip_backup_proxy_ip')
        backup_proxy_port = raw_config.get('sip_backup_proxy_port')
        outbound_proxy_ip = raw_config.get('sip_outbound_proxy_ip')
        outbound_proxy_port = raw_config.get('sip_outbound_proxy_port')
        voicemail = raw_config.get('exten_voicemail')

        for line in raw_config['sip_lines'].values():
            if proxy_ip:
                line.setdefault('proxy_ip', proxy_ip)
            if proxy_port:
                line.setdefault('proxy_port', proxy_port)
            if backup_proxy_ip:
                line.setdefault('backup_proxy_ip', backup_proxy_ip)
            if backup_proxy_port:
                line.setdefault('backup_proxy_port', backup_proxy_port)
            if outbound_proxy_ip:
                line.setdefault('outbound_proxy_ip', outbound_proxy_ip)
            if outbound_proxy_port:
                line.setdefault('outbound_proxy_port', outbound_proxy_port)
            if voicemail:
                line.setdefault('voicemail', voicemail)

    def _add_fkeys(self, raw_config, model):
        nb_funckeys = self._NB_FUNCKEYS.get(model)
        if not nb_funckeys:
            logger.warning(
                'Unknown model: "%s". Skipping function key configuration.', model
            )
            return

        raw_config['XX_fkeys'] = []
        for funckey_no, funckey_dict in raw_config['funckeys'].items():
            position = int(funckey_no) + 1
            fkey_type = self._FUNCKEY_TYPE.get(
                funckey_dict['type'], self._FUNCKEY_TYPE['speeddial']
            )
            fkey_label = funckey_dict['label']
            fkey_extension = funckey_dict['value']
            if position > nb_funckeys:
                logger.warning(
                    'Function key "%s" outside range supported by phone.', position
                )
                continue
            fkey_data = {
                'position': position,
                'type': fkey_type,
                'label': fkey_label,
                'extension': fkey_extension,
                'value': fkey_extension,
            }
            raw_config['XX_fkeys'].append(fkey_data)

    def _format_tzinfo(self, tzinfo):
        tz_hms = tzinfo['utcoffset'].as_hms
        offset_hour = tz_hms[0]
        offset_minutes = tz_hms[1]
        return f'{offset_hour:+02d}:{offset_minutes:02d}'

    def _add_timezone(self, raw_config):
        if 'timezone' in raw_config:
            try:
                tzinfo = tzinform.get_timezone_info(raw_config['timezone'])
            except tzinform.TimezoneNotFoundError as e:
                logger.warning('Unknown timezone "%s": "%s"', raw_config['timezone'], e)
            else:
                raw_config['XX_timezone'] = self._format_tzinfo(tzinfo)

    def _add_language(self, raw_config):
        locale = raw_config['locale']
        if '_' in locale:
            lang, _ = locale.split('_')
        else:
            lang = locale

        lang_code = self._LANG.get(lang, self._LANG['en'])
        raw_config['XX_lang'] = lang_code

    def _add_user_dtmf_info(self, raw_config):
        dtmf_mode = raw_config.get('sip_dtmf_mode')
        for line in raw_config['sip_lines'].values():
            cur_dtmf_mode = line.get('dtmf_mode', dtmf_mode)
            line['XX_user_dtmf_info'] = self._SIP_DTMF_MODE.get(cur_dtmf_mode, 'off')

    def _add_xivo_phonebook_url(self, raw_config):
        plugins.add_xivo_phonebook_url(raw_config, 'snom')

    def _check_config(self, raw_config):
        if 'http_port' not in raw_config:
            raise RawConfigError('only support configuration via HTTP')

    def _check_device(self, device):
        if 'mac' not in device:
            raise Exception('MAC address needed for device configuration')
        if 'model' not in device:
            raise Exception('Model name needed for device configuration')

    def _dev_specific_filename(self, device: dict[str, str]) -> str:
        return f'config.{format_mac(device["mac"], separator="")}.xml'

    def _add_server_url(self, raw_config: dict[str, Any]):
        if raw_config.get('http_base_url'):
            _, _, remaining_url = raw_config['http_base_url'].partition('://')
            raw_config['XX_server_url'] = raw_config['http_base_url']
            raw_config['XX_server_url_without_scheme'] = remaining_url
        else:
            base_url = f"{raw_config['ip']}:{raw_config['http_port']}"
            raw_config['XX_server_url_without_scheme'] = base_url
            raw_config['XX_server_url'] = f"http://{base_url}"

    def configure(self, device, raw_config):
        self._check_config(raw_config)
        self._check_device(device)
        xml_filename = self._dev_specific_filename(device)

        # generate xml file
        tpl = self._tpl_helper.get_dev_template(xml_filename, device)

        model = device.get('model')
        self._update_sip_lines(raw_config)
        self._add_fkeys(raw_config, model)
        self._add_timezone(raw_config)
        self._add_user_dtmf_info(raw_config)
        self._add_xivo_phonebook_url(raw_config)
        self._add_server_url(raw_config)
        self._add_language(raw_config)
        raw_config['XX_options'] = device.get('options', {})

        path = os.path.join(self._tftpboot_dir, xml_filename)
        self._tpl_helper.dump(tpl, raw_config, path, self._ENCODING)

    def deconfigure(self, device):
        filename = self._dev_specific_filename(device)
        try:
            os.remove(os.path.join(self._tftpboot_dir, filename))
        except OSError as e:
            # ignore
            logger.warning('error while removing file: "%s"', e)

    def synchronize(self, device, raw_config):
        return synchronize.standard_sip_synchronize(device, event='check-sync')

    def get_remote_state_trigger_filename(self, device):
        if 'mac' not in device:
            return None
        return self._dev_specific_filename(device)

    def is_sensitive_filename(self, filename):
        return bool(self._SENSITIVE_FILENAME_REGEX.match(filename))
