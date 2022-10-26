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
from typing import Dict, Optional

from provd import synchronize
from provd.devices.config import RawConfigError
from provd.plugins import StandardPlugin, FetchfwPluginHelper, TemplatePluginHelper
from provd.devices.pgasso import BasePgAssociator, DeviceSupport
from provd.servers.http import HTTPNoListingFileService
from provd.util import norm_mac, format_mac
from provd.servers.http_site import Request
from provd.devices.ident import RequestType
from twisted.internet import defer, threads

logger = logging.getLogger('plugin.xivo-panasonic')


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
        super().__init__(self)
        self._models = models
        self._version = version

    def _do_associate(
        self, vendor: str, model: Optional[str], version: Optional[str]
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

    def _dev_specific_filename(self, device: Dict[str, str]) -> str:
        # Return the device specific filename (not pathname) of device
        formatted_mac = format_mac(device['mac'], separator='', uppercase=True)
        return f'Config{formatted_mac}.cfg'

    def _check_config(self, raw_config):
        if 'http_port' not in raw_config:
            raise RawConfigError('only support configuration via HTTP')

    def _check_device(self, device: Dict[str, str]):
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

    def configure(self, device, raw_config):
        self._check_config(raw_config)
        self._check_device(device)
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

    if hasattr(synchronize, 'standard_sip_synchronize'):

        def synchronize(self, device, raw_config):
            return synchronize.standard_sip_synchronize(device)

    else:
        # backward compatibility with older wazo-provd server
        def synchronize(self, device, raw_config):
            try:
                ip = device['ip'].encode('ascii')
            except KeyError:
                return defer.fail(
                    Exception('IP address needed for device synchronization')
                )
            else:
                sync_service = synchronize.get_sync_service()
                if sync_service is None or sync_service.TYPE != 'AsteriskAMI':
                    return defer.fail(
                        Exception(f'Incompatible sync service: {sync_service}')
                    )
                return threads.deferToThread(sync_service.sip_notify, ip, 'check-sync')

    def get_remote_state_trigger_filename(self, device):
        if 'mac' not in device:
            return None

        return self._dev_specific_filename(device)
