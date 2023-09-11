# Copyright 2013-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import logging
import os.path
import re

from provd import plugins
from provd import synchronize
from provd import tzinform
from provd.devices.config import RawConfigError
from provd.plugins import FetchfwPluginHelper, StandardPlugin, TemplatePluginHelper
from provd.devices.pgasso import BasePgAssociator, DeviceSupport
from provd.servers.http import HTTPNoListingFileService
from provd.servers.http_site import Request
from provd.devices.ident import RequestType
from provd.util import norm_mac, format_mac
from twisted.internet import defer

logger = logging.getLogger('plugin.wazo-fanvil')


class BaseFanvilHTTPDeviceInfoExtractor:
    _PATH_REGEX = re.compile(r'\b(?!0{12})([\da-f]{12})\.cfg$')
    _UA_REGEX = re.compile(
        r'^Fanvil (?P<model>[XVi][0-9]{1,3}[WSGVUCi]?[DV]?[0-9]?( Pro)?(-V2)?) (?P<version>[0-9.]+) (?P<mac>[\da-f]{12})$'  # noqa: E501
    )

    def __init__(self, common_files):
        self._COMMON_FILES = common_files

    def extract(self, request: Request, request_type: RequestType):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request: Request):
        dev_info = {}
        dev_info.update(self._extract_from_path(request))
        ua = request.getHeader(b'User-Agent')
        if ua:
            dev_info.update(self._extract_from_ua(ua.decode('ascii')))

        return dev_info

    def _extract_from_ua(self, ua: str):
        # Fanvil X4 2.10.2.6887 0c383e07e16c
        # Fanvil X6U Pro 0.0.10 0c383e2cd782
        # Fanvil V67 2.6.6.187 0c383e2b29e6
        # Fanvil i10SV 2.12.10.1 0c383e2397f4
        # Fanvil i53W 2.12.9 0c383e10a440
        # Fanvil V65 2.12.2.4 0c383e38e123
		# Fanvil X4U-V2 2.12.16.17 0c383e43b71
		# Fanvil X5U-V2 2.12.16.17 0c383e32c10d
		# Fanvil X7-V2 2.12.16.17 0c383e32c10f

        dev_info = {}
        m = self._UA_REGEX.search(ua)
        if m:
            dev_info['vendor'] = 'Fanvil'
            dev_info['model'] = m.group('model').replace(' ', '-')
            dev_info['version'] = m.group('version')
            dev_info['mac'] = norm_mac(m.group('mac'))
        return dev_info

    def _extract_from_path(self, request: Request):
        filename = os.path.basename(request.path.decode('ascii'))
        device_info = self._COMMON_FILES.get(filename)
        if device_info:
            return {'vendor': 'Fanvil', 'model': device_info[0]}

        m = self._PATH_REGEX.search(request.path.decode('ascii'))
        if m:
            raw_mac = m.group(1)
            mac = norm_mac(raw_mac)
            return {'mac': mac}
        return {}


class BaseFanvilPgAssociator(BasePgAssociator):
    def __init__(self, models):
        super().__init__()
        self._models = models

    def _do_associate(
        self, vendor: str, model: str | None, version: str | None
    ) -> DeviceSupport:
        if vendor == 'Fanvil':
            if model in self._models:
                return DeviceSupport.COMPLETE
            return DeviceSupport.UNKNOWN
        return DeviceSupport.IMPROBABLE


class BaseFanvilPlugin(StandardPlugin):
    _ENCODING = 'UTF-8'
    _LOCALE = {}
    _TZ_INFO = {}
    _SIP_DTMF_MODE = {
        'RTP-in-band': '0',
        'RTP-out-of-band': '1',
        'SIP-INFO': '2',
    }
    _SIP_TRANSPORT = {
        'udp': '0',
        'tcp': '1',
        'tls': '3',
    }
    _DIRECTORY_KEY = {
        'en': 'Directory',
        'fr': 'Annuaire',
    }
    _NEW_MODEL_REGEX = re.compile(r'^X([4-9][UC]|(210i?)|7)([- ]Pro)?$')
    _NEW_MODEL_SHORT_LANGUAGE_MAPPINGS = {
        'ca': 'cat',
        'eu': 'eus',
        'sk': 'slo',
    }
    _NEW_SUPPORTED_LANGUAGES = (
        'en',
        'cn',
        'tc',
        'ru',
        'it',
        'fr',
        'de',
        'he',
        'es',
        'cat',
        'eus',
        'tr',
        'hr',
        'slo',
        'cz',
        'nl',
        'ko',
        'ua',
        'pt',
        'pl',
        'ar',
    )

    def __init__(self, app, plugin_dir, gen_cfg, spec_cfg):
        super().__init__(app, plugin_dir, gen_cfg, spec_cfg)
        # update to use the non-standard tftpboot directory
        self._base_tftpboot_dir = self._tftpboot_dir
        self._tftpboot_dir = os.path.join(self._tftpboot_dir, 'Fanvil')

        self._tpl_helper = TemplatePluginHelper(plugin_dir)

        downloaders = FetchfwPluginHelper.new_downloaders(gen_cfg.get('proxies'))
        fetchfw_helper = FetchfwPluginHelper(plugin_dir, downloaders)
        # update to use the non-standard tftpboot directory
        fetchfw_helper.root_dir = self._tftpboot_dir

        self.services = fetchfw_helper.services()
        self.http_service = HTTPNoListingFileService(self._base_tftpboot_dir)

    def _dev_specific_filename(self, device: dict[str, str]) -> str:
        # Return the device specific filename (not pathname) of device
        formatted_mac = format_mac(device['mac'], separator='', uppercase=False)
        return f'{formatted_mac}.cfg'

    def _check_config(self, raw_config):
        if 'http_port' not in raw_config:
            raise RawConfigError('only support configuration via HTTP')

    def _check_device(self, device):
        if 'mac' not in device:
            raise Exception('MAC address needed for device configuration')

    def _add_wazo_phoned_user_service_url(self, raw_config, service):
        if hasattr(plugins, 'add_wazo_phoned_user_service_url'):
            plugins.add_wazo_phoned_user_service_url(raw_config, 'yealink', service)

    def _add_server_url(self, raw_config):
        ip = raw_config['ip']
        http_port = raw_config['http_port']
        raw_config['XX_server_url'] = f'http://{ip}:{http_port}'

    def configure(self, device, raw_config):
        self._check_config(raw_config)
        self._check_device(device)
        self._check_lines_password(raw_config)
        self._add_timezone(device, raw_config)
        self._add_locale(device, raw_config)
        self._add_sip_transport(raw_config)
        self._update_lines(raw_config)
        self._add_fkeys(device, raw_config)
        self._add_phonebook_url(raw_config)
        self._add_wazo_phoned_user_service_url(raw_config, 'dnd')
        self._add_server_url(raw_config)
        self._add_firmware(device, raw_config)

        filename = self._dev_specific_filename(device)
        tpl = self._tpl_helper.get_dev_template(filename, device)

        path = os.path.join(self._tftpboot_dir, filename)
        self._tpl_helper.dump(tpl, raw_config, path, self._ENCODING)

    def deconfigure(self, device):
        self._remove_configuration_file(device)

    def configure_common(self, raw_config):
        self._add_server_url(raw_config)
        for filename, (
            model_info,
            fw_filename,
            tpl_filename,
        ) in self._COMMON_FILES.items():
            tpl = self._tpl_helper.get_template(f'common/{tpl_filename}')
            dst = os.path.join(self._tftpboot_dir, filename)
            raw_config['XX_fw_filename'] = fw_filename
            raw_config['XX_model_info'] = model_info
            self._tpl_helper.dump(tpl, raw_config, dst, self._ENCODING)

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

    def _check_lines_password(self, raw_config):
        for line in raw_config['sip_lines'].values():
            if line['password'] == 'autoprov':
                line['password'] = ''

    def _extract_dst_change(self, dst_change):
        lines = {}
        lines['month'] = dst_change['month']
        lines['hour'] = min(dst_change['time'].as_hours, 23)
        if dst_change['day'].startswith('D'):
            lines['dst_wday'] = dst_change['day'][1:]
        else:
            week, weekday = dst_change['day'][1:].split('.')
            if week == '5':
                lines['dst_week'] = -1
            else:
                lines['dst_week'] = week
            lines['dst_wday'] = int(weekday) - 1
        return lines

    def _extract_tzinfo(self, device, tzinfo):
        tz_all = {}
        utc = tzinfo['utcoffset'].as_hours
        utc_list = self._TZ_INFO[utc]
        for time_zone_name, time_zone in utc_list:
            tz_all['time_zone'] = time_zone
            tz_all['time_zone_name'] = time_zone_name

        if tzinfo['dst'] is None:
            tz_all['enable_dst'] = False
        else:
            tz_all['enable_dst'] = True
            tz_all['dst_min_offset'] = min(tzinfo['dst']['save'].as_minutes, 60)
            tz_all['dst_start'] = self._extract_dst_change(tzinfo['dst']['start'])
            tz_all['dst_end'] = self._extract_dst_change(tzinfo['dst']['end'])
        return tz_all

    def _add_timezone(self, device, raw_config):
        if 'timezone' in raw_config:
            try:
                tzinfo = tzinform.get_timezone_info(raw_config['timezone'])
            except tzinform.TimezoneNotFoundError as e:
                logger.info('Unknown timezone: %s', e)
            else:
                raw_config['XX_timezone'] = self._extract_tzinfo(device, tzinfo)

    def _is_new_model(self, device):
        return self._NEW_MODEL_REGEX.match(device['model']) is not None

    def _add_locale(self, device, raw_config):
        locale = raw_config.get('locale')
        if not locale:
            return
        language = locale.split('_')[0]
        if self._is_new_model(device):
            language = self._NEW_MODEL_SHORT_LANGUAGE_MAPPINGS.get(language, language)
            if language in self._NEW_SUPPORTED_LANGUAGES:
                raw_config['XX_locale'] = language
        elif locale in self._LOCALE:
            raw_config['XX_locale'] = self._LOCALE[locale]
        directory_key_text = self._DIRECTORY_KEY.get(language, None)
        if directory_key_text:
            raw_config['XX_directory'] = directory_key_text

    def _update_lines(self, raw_config):
        default_dtmf_mode = raw_config.get('sip_dtmf_mode', 'SIP-INFO')
        for line in raw_config['sip_lines'].values():
            line['XX_dtmf_mode'] = self._SIP_DTMF_MODE[
                line.get('dtmf_mode', default_dtmf_mode)
            ]
            line['backup_proxy_ip'] = line.get('backup_proxy_ip') or raw_config.get(
                'sip_backup_proxy_ip'
            )
            line['backup_proxy_port'] = line.get('backup_proxy_port') or raw_config.get(
                'sip_backup_proxy_port'
            )
            if 'voicemail' not in line and 'exten_voicemail' in raw_config:
                line['voicemail'] = raw_config['exten_voicemail']

    def _add_sip_transport(self, raw_config):
        raw_config['X_sip_transport_protocol'] = self._SIP_TRANSPORT[
            raw_config.get('sip_transport', 'udp')
        ]

    def _format_funckey_speeddial(self, funckey_dict):
        return '{value}@{line}/f'.format(
            value=funckey_dict['value'], line=funckey_dict['line']
        )

    def _format_funckey_blf(self, funckey_dict, exten_pickup_call=None):
        # Be warned that blf works only for DSS keys.
        if exten_pickup_call:
            return '{value}@{line}/ba{exten_pickup}{value}'.format(
                value=funckey_dict['value'],
                line=funckey_dict['line'],
                exten_pickup=exten_pickup_call,
            )
        else:
            return '{value}@{line}/ba'.format(
                value=funckey_dict['value'], line=funckey_dict['line']
            )

    def _format_funckey_call_park(self, funckey_dict):
        return '{value}@{line}/c'.format(
            value=funckey_dict['value'], line=funckey_dict['line']
        )

    def _add_fkeys(self, device, raw_config):
        lines = []
        exten_pickup_call = raw_config.get('exten_pickup_call')
        offset = 0 if self._is_new_model(device) else 1
        max_funckey_position = 0
        for funckey_no, funckey_dict in raw_config['funckeys'].items():
            fkey_line = {}
            keynum = int(funckey_no)
            fkey_id = keynum + offset
            fkey_line['id'] = fkey_id
            fkey_line['title'] = funckey_dict['label']
            fkey_line['type'] = 1
            if keynum > max_funckey_position:
                max_funckey_position = keynum

            funckey_type = funckey_dict['type']
            if funckey_type == 'speeddial':
                fkey_line['value'] = self._format_funckey_speeddial(funckey_dict)
                if funckey_dict['value'].startswith('*'):
                    fkey_line['type'] = 4
            elif funckey_type == 'blf':
                if keynum <= 12:
                    fkey_line['value'] = self._format_funckey_blf(
                        funckey_dict, exten_pickup_call
                    )
                else:
                    logger.info('For Fanvil, blf is only available on DSS keys')
                    fkey_line['value'] = self._format_funckey_speeddial(funckey_dict)
            elif funckey_type == 'park':
                fkey_line['value'] = self._format_funckey_call_park(funckey_dict)
            else:
                logger.info('Unsupported funckey type: %s', funckey_type)
                continue

            lines.append(fkey_line)

        keys_per_page = self._FUNCTION_KEYS_PER_PAGE.get(
            device['model'].split('-')[0], None
        )
        if keys_per_page:
            raw_config['XX_max_page'] = max_funckey_position // keys_per_page + 1
            raw_config['XX_paginated_fkeys'] = sorted(
                [
                    (
                        (fkey['id'] - 1) // keys_per_page,
                        (fkey['id'] - 1) % keys_per_page,
                        fkey,
                    )
                    for fkey in lines
                ]
            )
        else:
            raw_config['XX_paginated_fkeys'] = [
                (0, fkey['id'] - 1, fkey) for fkey in lines
            ]
        raw_config['XX_fkeys'] = lines

    def _add_phonebook_url(self, raw_config):
        if (
            hasattr(plugins, 'add_xivo_phonebook_url')
            and raw_config.get('config_version', 0) >= 1
        ):
            plugins.add_xivo_phonebook_url(raw_config, 'fanvil')

    def _add_firmware(self, device, raw_config):
        model = device.get('model')
        if model in self._MODEL_FIRMWARE_MAPPING:
            raw_config['XX_fw_filename'] = self._MODEL_FIRMWARE_MAPPING[model]
