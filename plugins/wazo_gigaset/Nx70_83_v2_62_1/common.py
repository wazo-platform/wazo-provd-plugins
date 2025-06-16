# Copyright 2011-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Common code shared by the various wazo-gigaset plugins.
"""
from __future__ import annotations

import logging
import os
import re
import time

try:
    from wazo_provd import plugins, synchronize, tzinform
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
    from provd import plugins, synchronize, tzinform
    from provd.devices.ident import RequestType
    from provd.devices.pgasso import BasePgAssociator, DeviceSupport
    from provd.plugins import FetchfwPluginHelper, StandardPlugin, TemplatePluginHelper
    from provd.servers.http import HTTPNoListingFileService
    from provd.servers.http_site import Request
    from provd.util import format_mac, norm_mac

from twisted.internet import defer

logger = logging.getLogger('plugin.wazo-gigaset')

VENDOR = 'Gigaset'


class GigasetHTTPDeviceInfoExtractor:
    _UA_REGEX = re.compile(
        r'^"?(Gigaset )?(?P<model>[\w\s]+)\/(?P<version>(?:\w{2,3}\.){3,4}\w{1,3})(?:\+.+)?;'
        r'(?P<mac>[0-9A-F]{12})?(;Handset=\d+)?"?$'
    )

    def extract(self, request: Request, request_type: RequestType):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request: Request):
        dev_info = {}

        ua = request.getHeader(b'User-Agent')
        if ua:
            dev_info.update(self._extract_from_ua(ua.decode('ascii')))

        return dev_info

    def _extract_from_ua(self, ua: str):
        # HTTP User-Agent:
        # "Gigaset N870 IP PRO/83.V2.11.0+build.a546b91;7C2F80E0D605"
        m = self._UA_REGEX.search(ua)
        dev_info = {}
        if m:
            dev_info = {
                'vendor': VENDOR,
                'model': m.group('model'),
                'version': m.group('version'),
            }
            if 'mac' in m.groupdict():
                dev_info['mac'] = norm_mac(m.group('mac'))

        return dev_info


class BaseGigasetPgAssociator(BasePgAssociator):
    def __init__(self, models):
        self._models = models

    def _do_associate(
        self, vendor: str, model: str | None, version: str | None
    ) -> DeviceSupport:
        if vendor == VENDOR:
            if model in self._models:
                if version == self._models[model]:
                    return DeviceSupport.EXACT
                return DeviceSupport.COMPLETE
            return DeviceSupport.UNKNOWN
        return DeviceSupport.IMPROBABLE


class BaseGigasetPlugin(StandardPlugin):
    _ENCODING = 'UTF-8'

    _LOCALE = {
        'de_DE': 'Germany',
        'en_US': 'Retail',
        'es_ES': 'Spain',
        'fr_FR': 'France',
        'fr_CA': 'Retail',
    }
    _SIP_DTMF_MODE = {
        'RTP-in-band': '1',
        'RTP-out-of-band': '2',
        'SIP-INFO': '4',
    }
    _SIP_TRANSPORT = {
        'udp': '1',
        'tcp': '2',
        'tls': '3',
    }

    _VALID_TZ_GIGASET = {
        'Pacific/Honolulu',
        'America/Anchorage',
        'America/Los_Angeles',
        'America/Denver',
        'America/Chicago',
        'America/New_York',
        'America/Caracas',
        'America/Sao_Paulo',
        'Europe/Belfast',
        'Europe/Dublin',
        'Europe/Guernsey',
        'Europe/Isle_of_Man',
        'Europe/Jersey',
        'Europe/Lisbon',
        'Europe/London',
        'Greenwich',
        'Europe/Amsterdam',
        'Europe/Andorra',
        'Europe/Belgrade',
        'Europe/Berlin',
        'Europe/Bratislava',
        'Europe/Brussels',
        'Europe/Budapest',
        'Europe/Busingen',
        'Europe/Copenhagen',
        'Europe/Gibraltar',
        'Europe/Ljubljana',
        'Europe/Luxembourg',
        'Europe/Madrid',
        'Europe/Malta',
        'Europe/Monaco',
        'Europe/Oslo',
        'Europe/Paris',
        'Europe/Podgorica',
        'Europe/Prague',
        'Europe/Rome',
        'Europe/San_Marino',
        'Europe/Sarajevo',
        'Europe/Skopje',
        'Europe/Stockholm',
        'Europe/Tirane',
        'Europe/Vaduz',
        'Europe/Vatican',
        'Europe/Vienna',
        'Europe/Warsaw',
        'Europe/Zagreb',
        'Europe/Zurich',
        'Africa/Cairo',
        'Europe/Athens',
        'Europe/Bucharest',
        'Europe/Chisinau',
        'Europe/Helsinki',
        'Europe/Kaliningrad',
        'Europe/Kiev',
        'Europe/Mariehamn',
        'Europe/Nicosia',
        'Europe/Riga',
        'Europe/Sofia',
        'Europe/Tallinn',
        'Europe/Tiraspol',
        'Europe/Uzhgorod',
        'Europe/Vilnius',
        'Europe/Zaporozhye',
        'Europe/Istanbul',
        'Europe/Kirov',
        'Europe/Minsk',
        'Europe/Moscow',
        'Europe/Simferopol',
        'Europe/Volgograd',
        'Asia/Dubai',
        'Europe/Astrakhan',
        'Europe/Samara',
        'Europe/Ulyanovsk',
        'Asia/Karachi',
        'Asia/Dhaka',
        'Asia/Hong_Kong',
        'Asia/Tokyo',
        'Australia/Adelaide',
        'Australia/Darwin',
        'Australia/Brisbane',
        'Australia/Sydney',
        'Pacific/Noumea',
    }

    _FALLBACK_TZ = {
        (-3, 0): 'America/Sao_Paulo',
        (-4, 0): 'America/New_York',
        (-5, 0): 'America/Chicago',
        (-6, 0): 'America/Denver',
        (-7, 0): 'America/Los_Angeles',
        (-8, 0): 'America/Anchorage',
        (-10, 0): 'Pacific/Honolulu',
        (0, 0): 'Greenwich',
        (1, 0): 'Europe/London',
        (2, 0): 'Europe/Paris',
        (3, 0): 'Europe/Moscow',
        (4, 0): 'Asia/Dubai',
        (5, 0): 'Asia/Karachi',
        (6, 0): 'Asia/Dhaka',
        (8, 0): 'Asia/Hong_Kong',
        (9, 0): 'Asia/Tokyo',
        (9, 3): 'Australia/Adelaide',
        (10, 0): 'Australia/Sydney',
        (11, 0): 'Pacific/Noumea',
    }
    _SENSITIVE_FILENAME_REGEX = re.compile(r'^[0-9a-f]{12}\.xml$')

    def __init__(self, app, plugin_dir, gen_cfg, spec_cfg):
        super().__init__(app, plugin_dir, gen_cfg, spec_cfg)
        self._app = app

        self._tpl_helper = TemplatePluginHelper(plugin_dir)
        downloaders = FetchfwPluginHelper.new_downloaders(gen_cfg.get('proxies'))
        fetchfw_helper = FetchfwPluginHelper(plugin_dir, downloaders)

        self.services = fetchfw_helper.services()
        self.http_service = HTTPNoListingFileService(self._tftpboot_dir)

    http_dev_info_extractor = GigasetHTTPDeviceInfoExtractor()

    def _check_device(self, device):
        if 'ip' not in device:
            raise Exception('IP address needed for Gigaset configuration')

    def _dev_specific_filename(self, device: dict[str, str]) -> str:
        # Return the device specific filename (not pathname) of device
        formatted_mac = format_mac(device['mac'], separator='', uppercase=False)
        return f'{formatted_mac}.xml'

    def _add_phonebook(self, raw_config):
        uuid_format = '{scheme}://{hostname}:{port}/0.1/directories/lookup/{profile}/gigaset/{user_uuid}?'  # noqa: E501
        plugins.add_xivo_phonebook_url_from_format(raw_config, uuid_format)

    def _add_country_and_lang(self, raw_config):
        locale = raw_config.get('locale')
        if locale in self._LOCALE:
            raw_config['XX_country'] = self._LOCALE[locale]
        else:
            raw_config['XX_country'] = 'Retail'

    def _fix_timezone(self, raw_config):
        timezone = raw_config.get('timezone', 'Greenwich')
        if timezone not in self._VALID_TZ_GIGASET:
            tz_db = tzinform.TextTimezoneInfoDB()
            tz_info = tz_db.get_timezone_info(timezone)['utcoffset'].as_hms
            offset_hour = tz_info[0]
            offset_minutes = tz_info[1]
            raw_config['timezone'] = self._FALLBACK_TZ[(offset_hour, offset_minutes)]

    def _add_xx_vars(self, device, raw_config):
        raw_config['XX_epoch'] = int(time.time())
        self._fix_timezone(raw_config)

        if raw_config.get('http_base_url'):
            _, _, remaining_url = raw_config['http_base_url'].partition('://')
            raw_config['XX_server_url'] = raw_config['http_base_url']
            raw_config['XX_server_url_without_scheme'] = remaining_url
        else:
            base_url = f"{raw_config['ip']}:{raw_config['http_port']}"
            raw_config['XX_server_url_without_scheme'] = base_url
            raw_config['XX_server_url'] = f"http://{base_url}"

    def _add_voip_providers(self, raw_config):
        voip_providers = dict()
        provider_id = 0
        sip_lines = raw_config.get('sip_lines')
        dtmf_mode = raw_config.get('sip_dtmf_mode', '1')
        sip_transport = self._SIP_TRANSPORT.get(raw_config.get('sip_transport', '1'))
        if sip_lines:
            for line in sip_lines.values():
                proxy_ip = line.get('proxy_ip')
                proxy_port = line.get('proxy_port', 5060)
                line_dtmf_mode = self._SIP_DTMF_MODE.get(
                    line.get('dtmf_mode', dtmf_mode)
                )
                if (proxy_ip, proxy_port) not in voip_providers:
                    provider = {
                        'id': provider_id,
                        'sip_proxy_ip': proxy_ip,
                        'sip_proxy_port': proxy_port,
                        'dtmf_mode': line_dtmf_mode,
                        'sip_transport': sip_transport,
                    }
                    line['provider_id'] = provider_id
                    voip_providers[(proxy_ip, proxy_port)] = provider
                    provider_id += 1
                else:
                    line['provider_id'] = voip_providers[(proxy_ip, proxy_port)]['id']

        raw_config['XX_voip_providers'] = list(voip_providers.values())

    def _add_ac_code(self, raw_config):
        sip_lines = raw_config.get('sip_lines')
        if sip_lines:
            for line in sip_lines.values():
                number = line.get('number')
                if number.startswith('auto'):
                    line['XX_hs_code'] = '0000'
                else:
                    line['XX_hs_code'] = number[-4:].zfill(4)

    def configure(self, device, raw_config):
        self._check_device(device)
        filename = self._dev_specific_filename(device)
        tpl = self._tpl_helper.get_dev_template(filename, device)

        self._add_country_and_lang(raw_config)
        self._add_voip_providers(raw_config)
        self._add_ac_code(raw_config)
        self._add_xx_vars(device, raw_config)
        self._add_phonebook(raw_config)

        path = os.path.join(self._tftpboot_dir, filename)
        self._tpl_helper.dump(tpl, raw_config, path, self._ENCODING)

    def deconfigure(self, device):
        path = os.path.join(self._tftpboot_dir, self._dev_specific_filename(device))
        try:
            os.remove(path)
        except OSError as e:
            logger.info('error while removing configuration file: %s', e)

    def is_sensitive_filename(self, filename):
        return bool(self._SENSITIVE_FILENAME_REGEX.match(filename))

    def synchronize(self, device, raw_config):
        return synchronize.standard_sip_synchronize(device)
