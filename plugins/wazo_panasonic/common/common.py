# Copyright 2010-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
import os.path
import re

try:
    from wazo_provd import synchronize
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
    from wazo_provd.util import format_mac, norm_mac
except ImportError:
    # Compatibility with wazo < 24.02
    from provd import synchronize
    from provd.devices.config import RawConfigError
    from provd.devices.ident import RequestType
    from provd.devices.pgasso import BasePgAssociator, DeviceSupport
    from provd.plugins import FetchfwPluginHelper, StandardPlugin, TemplatePluginHelper
    from provd.servers.http import HTTPNoListingFileService
    from provd.servers.http_site import Request
    from provd.util import format_mac, norm_mac

from twisted.internet import defer

logger = logging.getLogger('plugin.wazo-panasonic')


class BasePanasonicHTTPDeviceInfoExtractor:
    _UA_REGEX = re.compile(r'^Panasonic_([^ ]+)/([^ ]+) \(([^ ]+)\)')

    def extract(self, request: Request, request_type: RequestType):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request: Request):
        ua = request.getHeader(b'User-Agent')
        if ua:
            return self._extract_from_ua(ua.decode('ascii'))
        return None

    def _extract_from_ua(self, ua: str):
        # HTTP User-Agent:
        # "Panasonic_KX-UT113/01.133 (0080f0c8c381)"
        m = self._UA_REGEX.match(ua)
        if m:
            model, version, raw_mac = m.groups()
            try:
                mac = norm_mac(raw_mac)
            except ValueError as e:
                logger.warning('Could not normalize MAC address: %s', e)
            else:
                return {
                    'vendor': 'Panasonic',
                    'model': model,
                    'version': version,
                    'mac': mac,
                }
        return None


class BasePanasonicPgAssociator(BasePgAssociator):
    def __init__(self, models, version):
        super().__init__()
        self._models = models
        self._version = version

    def _do_associate(
        self, vendor: str, model: str | None, version: str | None
    ) -> DeviceSupport:
        if vendor == 'Panasonic':
            if model in self._models:
                if version == self._version:
                    return DeviceSupport.EXACT
                return DeviceSupport.COMPLETE
            return DeviceSupport.UNKNOWN
        return DeviceSupport.IMPROBABLE


class BasePanasonicPlugin(StandardPlugin):
    _ENCODING = 'UTF-8'
    _tftpboot_dir: str

    def __init__(self, app, plugin_dir, gen_cfg, spec_cfg):
        super().__init__(app, plugin_dir, gen_cfg, spec_cfg)
        # update to use the non-standard tftpboot directory
        self._base_tftpboot_dir = self._tftpboot_dir
        self._tftpboot_dir = os.path.join(self._tftpboot_dir, 'Panasonic')

        self._tpl_helper = TemplatePluginHelper(plugin_dir)

        downloaders = FetchfwPluginHelper.new_downloaders(gen_cfg.get('proxies'))
        fetchfw_helper = FetchfwPluginHelper(plugin_dir, downloaders)
        # update to use the non-standard tftpboot directory
        fetchfw_helper.root_dir = self._tftpboot_dir

        self.services = fetchfw_helper.services()
        self.http_service = HTTPNoListingFileService(self._base_tftpboot_dir)

    http_dev_info_extractor = BasePanasonicHTTPDeviceInfoExtractor()

    def _dev_specific_filename(self, device: dict[str, str]) -> str:
        # Return the device specific filename (not pathname) of device
        formatted_mac = format_mac(device['mac'], separator='', uppercase=True)
        return f'Config{formatted_mac}.cfg'

    def _check_config(self, raw_config):
        if 'http_port' not in raw_config:
            raise RawConfigError('only support configuration via HTTP')

    def _check_device(self, device: dict[str, str]):
        if 'mac' not in device:
            raise Exception('MAC address needed for device configuration')

    def _common_templates(self):
        for tpl_format, file_format in [
            ('common/%s.tpl', '%s.cfg'),
        ]:
            for model in self._MODELS:
                yield tpl_format % model, file_format % model

    def configure_common(self, raw_config):
        for tpl_filename, filename in self._common_templates():
            tpl = self._tpl_helper.get_template(tpl_filename)
            dst = os.path.join(self._base_tftpboot_dir, filename)
            self._tpl_helper.dump(tpl, raw_config, dst, self._ENCODING)

    def _add_server_url(self, raw_config):
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
        self._add_server_url(raw_config)
        filename = self._dev_specific_filename(device)
        tpl = self._tpl_helper.get_dev_template(filename, device)

        path = os.path.join(self._tftpboot_dir, filename)
        self._tpl_helper.dump(tpl, raw_config, path, self._ENCODING)

    def deconfigure(self, device):
        self._remove_configuration_file(device)

    def _remove_configuration_file(self, device):
        path = os.path.join(self._tftpboot_dir, self._dev_specific_filename(device))
        try:
            os.remove(path)
        except OSError as e:
            logger.info('error while removing configuration file: %s', e)

    def synchronize(self, device, raw_config):
        return synchronize.standard_sip_synchronize(device)

    def get_remote_state_trigger_filename(self, device):
        if 'mac' not in device:
            return None
        return self._dev_specific_filename(device)
