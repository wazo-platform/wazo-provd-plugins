# Copyright 2011-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

"""Common code shared by the various wazo-avaya plugins.

Support the 1220IP and 1230IP.
Support the J129, J169 and J179

"""
from __future__ import annotations

import logging
import os
import re

try:
    from wazo_provd import synchronize, tzinform
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
    from provd import synchronize, tzinform
    from provd.devices.config import RawConfigError
    from provd.devices.ident import RequestType
    from provd.devices.pgasso import BasePgAssociator, DeviceSupport
    from provd.plugins import FetchfwPluginHelper, StandardPlugin, TemplatePluginHelper
    from provd.servers.http import HTTPNoListingFileService
    from provd.servers.http_site import Request
    from provd.servers.tftp.service import TFTPFileService, TFTPRequest
    from provd.util import format_mac, norm_mac

from twisted.internet import defer

logger = logging.getLogger('plugin.wazo-avaya')


_FILENAME_MAP = {
    '1220.cfg': '1220IP',
    '1220SIP.cfg': '1220IP',
    '1230.cfg': '1230IP',
    '1230SIP.cfg': '1230IP',
    'J100Supgrade.txt': 'J129',
    'J100Supgrade.txt': 'J169',
    'J100Supgrade.txt': 'J179',
}


class BaseAvayaHTTPDeviceInfoExtractor:
    _UA_REGEX = [
        re.compile(r'^AVAYA/[^/]+/([\d.]{11})$'),
        re.compile(r'(?<=)AVAYA\/+(\w+)\-+([\d.]+)\s+\(MAC\:([\da-fA-F]{12})\)$')
    ]

    _PATH_REGEX = re.compile(r'\bSIP([\dA-F]{12})\.cfg$')

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
        # HTTP User-Agent:
        #   "AVAYA/SIP12x0\x17/04.00.04.00"
        #   "AVAYA/SIP12x0\x16/04.00.04.00"
        #   "AVAYA/SIP12x0\x14/04.00.04.00"
        #   "AVAYA/SIP12x0\xff/04.01.13.00"
        #   "Mozilla/4.0 (compatible; MSIE 6.0) AVAYA/J179-4.1.3.0.6 (MAC:c81fea83e85a)"
        m = self._UA_REGEX.match(ua)
        if m:
            return {'vendor': 'Avaya', 'version': m.group(1)}
        return None

    def _extract_from_path(self, path: str, dev_info: dict[str, str]):
        m = self._PATH_REGEX.search(path)
        if m:
            dev_info['mac'] = norm_mac(m.group(1))
        else:
            filename = os.path.basename(path)
            if filename in _FILENAME_MAP:
                dev_info['model'] = _FILENAME_MAP[filename]


class BaseAvayaTFTPDeviceInfoExtractor:
    # TFTP is only used for the update from UNIStim to SIP, so we only
    # need minimal information to get the plugin association working.

    def extract(self, request: TFTPRequest, request_type: RequestType):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request: TFTPRequest):
        filename = request['packet']['filename'].decode('ascii')
        if filename in _FILENAME_MAP:
            return {'vendor': 'Avaya', 'model': _FILENAME_MAP[filename]}
        return None


class BaseAvayaPgAssociator(BasePgAssociator):
    def __init__(self, models, version):
        super().__init__()
        self._models = models
        self._version = version

    def _do_associate(
        self, vendor: str, model: str | None, version: str | None
    ) -> DeviceSupport:
        if vendor == 'Avaya':
            if model in self._models:
                if version == self._version:
                    return DeviceSupport.EXACT
                # XXX if there's one day a plugin supporting UNIStim (...),
                #     then we might want to do more check on the version,
                #     or return a lower support value
                return DeviceSupport.COMPLETE
            return DeviceSupport.PROBABLE
        return DeviceSupport.IMPROBABLE


class BaseAvayaPlugin(StandardPlugin):
    # XXX file encoding is not stated anywhere
    _ENCODING = 'UTF-8'

    def __init__(self, app, plugin_dir, gen_cfg, spec_cfg):
        super().__init__(app, plugin_dir, gen_cfg, spec_cfg)

        self._tpl_helper = TemplatePluginHelper(plugin_dir)

        downloaders = FetchfwPluginHelper.new_downloaders(gen_cfg.get('proxies'))
        fetchfw_helper = FetchfwPluginHelper(plugin_dir, downloaders)

        self.services = fetchfw_helper.services()
        self.tftp_service = TFTPFileService(self._tftpboot_dir)
        self.http_service = HTTPNoListingFileService(self._tftpboot_dir)

    http_dev_info_extractor = BaseAvayaHTTPDeviceInfoExtractor()

    tftp_dev_info_extractor = BaseAvayaTFTPDeviceInfoExtractor()

    def _add_timezone(self, raw_config):
        if 'timezone' in raw_config:
            try:
                tzinfo = tzinform.get_timezone_info(raw_config['timezone'])
            except tzinform.TimezoneNotFoundError as e:
                logger.warning('Unknown timezone: %s', e)
            else:
                raw_config[
                    'XX_timezone'
                ] = f'TIMEZONE_OFFSET {tzinfo["utcoffset"].as_seconds:d}'

    def _dev_specific_filename(self, device: dict[str, str]) -> str:
        # Return the device specific filename (not pathname) of device
        formatted_mac = format_mac(device['mac'], separator='', uppercase=True)
        return f'SIP{formatted_mac}.cfg'

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
