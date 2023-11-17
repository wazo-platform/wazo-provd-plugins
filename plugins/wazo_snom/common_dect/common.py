# Copyright 2010-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import logging
import os.path
import re

from pkg_resources import parse_version
from provd import plugins
from provd import synchronize
from provd.devices.config import RawConfigError
from provd.devices.pgasso import BasePgAssociator, DeviceSupport
from provd.plugins import (
    FetchfwPluginHelper,
    StandardPlugin,
    TemplatePluginHelper,
)
from provd.servers.http import HTTPNoListingFileService
from provd.servers.http_site import Request
from provd.devices.ident import RequestType
from provd.util import norm_mac, format_mac
from twisted.internet import defer

logger = logging.getLogger('plugin.wazo-snom')


class BaseSnomDECTHTTPDeviceInfoExtractor:
    _UA_REGEX_MAC = re.compile(
        r'\b[sS]nom\s?(?P<model>M[0-9]{3})\s(?P<version>[0-9.]+)\s(?P<mac>[0-9a-fA-F]{12})\b'
    )
    _PATH_REGEX = re.compile(r'\bsnom\w+-([\dA-F]{12})\.htm$')

    def extract(self, request: Request, request_type: RequestType):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request: Request):
        device_info = {}
        ua = request.getHeader(b'User-Agent')
        raw_mac: bytes = request.args.get(b'mac', [None])[0]
        if raw_mac:
            logger.debug('Got MAC from URL: %s', raw_mac)
            device_info['mac'] = norm_mac(raw_mac.decode('ascii'))
        if ua:
            info_from_ua = self._extract_from_ua(ua.decode('ascii'))
            if info_from_ua:
                device_info.update(info_from_ua)
                self._extract_from_path(request.path.decode('ascii'), device_info)
        return device_info

    def _extract_from_ua(self, ua: str):
        # HTTP User-Agent:
        #   "Mozilla/4.0 (compatible; Snom M900 05.20.0001 000413b60680)"
        m = self._UA_REGEX_MAC.search(ua)
        if m:
            raw_model, raw_version, raw_mac = m.groups()
            return {
                'vendor': 'Snom',
                'model': raw_model,
                'mac': norm_mac(raw_mac),
                'version': raw_version,
            }
        return None

    def _extract_from_path(self, path: str, dev_info: dict[str, str]):
        m = self._PATH_REGEX.search(path)
        if m:
            raw_mac = m.group(1)
            dev_info['mac'] = norm_mac(raw_mac)


class BaseSnomPgAssociator(BasePgAssociator):
    def __init__(self, models, version):
        self._models = models
        self._version = version

    def _do_associate(
        self, vendor: str, model: str | None, version: str | None
    ) -> DeviceSupport:
        if vendor == 'Snom':
            if version is None:
                # Could be an old version with no XML support
                return DeviceSupport.PROBABLE
            assert version is not None
            if self._is_incompatible_version(version):
                return DeviceSupport.NONE
            if model in self._models:
                if version == self._version:
                    return DeviceSupport.EXACT
                return DeviceSupport.COMPLETE
            return DeviceSupport.PROBABLE
        return DeviceSupport.IMPROBABLE

    def _is_incompatible_version(self, version):
        try:
            maj_version = parse_version(version)
            if maj_version < parse_version('05.00.0001'):
                return True
        except (IndexError, ValueError):
            pass
        return False


class BaseSnomPlugin(StandardPlugin):
    _ENCODING = 'UTF-8'
    _LOCALE = {
        'de_DE': ('Deutsch', 'GER'),
        'en_US': ('English', 'USA'),
        'es_ES': ('Espanol', 'ESP'),
        'fr_FR': ('Francais', 'FRA'),
        'fr_CA': ('Francais', 'USA'),
        'it_IT': ('Italiano', 'ITA'),
        'nl_NL': ('Dutch', 'NLD'),
    }
    _SIP_DTMF_MODE = {
        'RTP-in-band': 'off',
        'RTP-out-of-band': 'off',
        'SIP-INFO': 'sip_info_only',
    }
    _XX_DICT_DEF = 'en'
    _XX_DICT = {
        'en': {
            'remote_directory': 'Directory',
        },
        'fr': {
            'remote_directory': 'Annuaire',
        },
    }

    def __init__(self, app, plugin_dir, gen_cfg, spec_cfg):
        super().__init__(app, plugin_dir, gen_cfg, spec_cfg)

        self._tpl_helper = TemplatePluginHelper(plugin_dir)

        downloaders = FetchfwPluginHelper.new_downloaders(gen_cfg.get('proxies'))
        fetchfw_helper = FetchfwPluginHelper(plugin_dir, downloaders)

        self.services = fetchfw_helper.services()
        self.http_service = HTTPNoListingFileService(self._tftpboot_dir)

    http_dev_info_extractor = BaseSnomDECTHTTPDeviceInfoExtractor()

    def _common_templates(self):
        yield 'common/snom-general.xml.tpl', 'snom-general.xml'
        for tpl_format, file_format in [
            ('common/snom%s.htm.tpl', 'snom%s.htm'),
            ('common/snom%s.xml.tpl', 'snom%s.xml'),
            ('common/snom%s-firmware.xml.tpl', 'snom%s-firmware.xml'),
        ]:
            for model in self._MODELS:
                yield tpl_format % model, file_format % model

    def configure_common(self, raw_config):
        self._add_server_url(raw_config)
        for tpl_filename, filename in self._common_templates():
            tpl = self._tpl_helper.get_template(tpl_filename)
            dst = os.path.join(self._tftpboot_dir, filename)
            self._tpl_helper.dump(tpl, raw_config, dst, self._ENCODING)

    def _update_sip_lines(self, raw_config):
        proxy_ip = raw_config.get('sip_proxy_ip')
        backup_proxy_ip = raw_config.get('sip_backup_proxy_ip')
        voicemail = raw_config.get('exten_voicemail')
        for line in raw_config['sip_lines'].values():
            if proxy_ip:
                line.setdefault('proxy_ip', proxy_ip)
            if backup_proxy_ip:
                line.setdefault('backup_proxy_ip', backup_proxy_ip)
            if voicemail:
                line.setdefault('voicemail', voicemail)
            # set SIP server to use
            server_id = (
                raw_config['XX_servers']
                .get((line.get('proxy_ip'), line.get('proxy_port', 5060)), {})
                .get('id')
            )
            line['XX_server_id'] = server_id or 1

    def _add_sip_servers(self, raw_config):
        servers = {}
        server_number = 1
        for line_no, line in raw_config['sip_lines'].items():
            proxy_ip = line.get('proxy_ip') or raw_config.get('sip_proxy_ip')
            proxy_port = line.get('proxy_port') or raw_config.get('sip_proxy_port')
            backup_proxy_ip = line.get('backup_proxy_ip') or raw_config.get(
                'sip_backup_proxy_ip'
            )
            backup_proxy_port = line.get('backup_proxy_port') or raw_config.get(
                'sip_backup_proxy_port'
            )
            dtmf_mode = self._SIP_DTMF_MODE.get(
                line.get('dtmf_mode') or raw_config.get('sip_dtmf_mode'),
                'off',
            )
            if (proxy_ip, proxy_port) not in servers:
                servers[(proxy_ip, proxy_port)] = {
                    'id': server_number,
                    'proxy_ip': proxy_ip,
                    'proxy_port': proxy_port,
                    'backup_proxy_ip': backup_proxy_ip,
                    'backup_proxy_port': backup_proxy_port,
                    'dtmf_mode': dtmf_mode,
                }
            server_number += 1
            if server_number > 10:
                logger.warning('Maximum number of valid server reached')
        raw_config['XX_servers'] = servers

    def _format_fkey_value(self, fkey_type, value, suffix):
        return f'{fkey_type} {value}{suffix}'

    def _add_lang(self, raw_config):
        if 'locale' in raw_config:
            locale = raw_config['locale']
            if locale in self._LOCALE:
                raw_config['XX_lang'] = self._LOCALE[locale]

    def _add_user_dtmf_info(self, raw_config):
        dtmf_mode = raw_config.get('sip_dtmf_mode')
        for line in raw_config['sip_lines'].values():
            cur_dtmf_mode = line.get('dtmf_mode', dtmf_mode)
            line['XX_user_dtmf_info'] = self._SIP_DTMF_MODE.get(cur_dtmf_mode, 'off')

    def _add_xivo_phonebook_url(self, raw_config):
        plugins.add_xivo_phonebook_url(raw_config, 'snom')

    def _add_server_url(self, raw_config):
        if raw_config.get('http_base_url'):
            _, _, remaining_url = raw_config['http_base_url'].partition('://')
            raw_config['XX_server_url'] = raw_config['http_base_url']
            raw_config['XX_server_url_without_scheme'] = remaining_url
        else:
            base_url = f"{raw_config['ip']}:{raw_config['http_port']}"
            raw_config['XX_server_url_without_scheme'] = base_url
            raw_config['XX_server_url'] = f"http://{base_url}"

    def _gen_xx_dict(self, raw_config):
        xx_dict = self._XX_DICT[self._XX_DICT_DEF]
        if 'locale' in raw_config:
            locale = raw_config['locale']
            lang = locale.split('_', 1)[0]
            if lang in self._XX_DICT:
                xx_dict = self._XX_DICT[lang]
        return xx_dict

    _SENSITIVE_FILENAME_REGEX = re.compile(r'^[0-9A-F]{12}\.xml')

    def _dev_specific_filenames(self, device):
        # Return a tuple (htm filename, xml filename)
        formatted_mac = format_mac(device['mac'], separator='', uppercase=True)
        return f'snom{device["model"]}-{formatted_mac}.htm', f'{formatted_mac}.xml'

    def _check_config(self, raw_config):
        if 'http_port' not in raw_config:
            raise RawConfigError('only support configuration via HTTP')

    def _check_device(self, device):
        if 'mac' not in device:
            raise Exception('MAC address needed for device configuration')
        # model is needed since filename has model name in it.
        if 'model' not in device:
            raise Exception('model needed for device configuration')

    def configure(self, device, raw_config):
        self._check_config(raw_config)
        self._check_device(device)
        htm_filename, xml_filename = self._dev_specific_filenames(device)

        # generate xml file
        tpl = self._tpl_helper.get_dev_template(xml_filename, device)

        self._add_sip_servers(raw_config)
        self._update_sip_lines(raw_config)
        self._add_lang(raw_config)
        self._add_xivo_phonebook_url(raw_config)
        self._add_server_url(raw_config)
        raw_config['XX_dict'] = self._gen_xx_dict(raw_config)
        raw_config['XX_options'] = device.get('options', {})

        path = os.path.join(self._tftpboot_dir, xml_filename)
        self._tpl_helper.dump(tpl, raw_config, path, self._ENCODING)

        # generate htm file
        tpl = self._tpl_helper.get_template('other/base.htm.tpl')

        raw_config['XX_xml_filename'] = xml_filename

        path = os.path.join(self._tftpboot_dir, htm_filename)
        self._tpl_helper.dump(tpl, raw_config, path, self._ENCODING)

    def deconfigure(self, device):
        for filename in self._dev_specific_filenames(device):
            try:
                os.remove(os.path.join(self._tftpboot_dir, filename))
            except OSError as e:
                # ignore
                logger.info('error while removing file: %s', e)

    def synchronize(self, device, raw_config):
        return synchronize.standard_sip_synchronize(
            device, event='check-sync;reboot=true'
        )

    def get_remote_state_trigger_filename(self, device):
        if 'mac' not in device or 'model' not in device:
            return None

        return self._dev_specific_filenames(device)[1]

    def is_sensitive_filename(self, filename):
        return bool(self._SENSITIVE_FILENAME_REGEX.match(filename))
