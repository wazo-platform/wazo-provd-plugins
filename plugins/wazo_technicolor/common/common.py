# Copyright 2011-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import logging
import os.path
import re
import time

from provd import plugins, synchronize, tzinform
from provd.devices.config import RawConfigError
from provd.devices.ident import RequestType
from provd.devices.pgasso import BasePgAssociator, DeviceSupport
from provd.plugins import FetchfwPluginHelper, StandardPlugin, TemplatePluginHelper
from provd.servers.http import HTTPNoListingFileService
from provd.servers.http_site import Request
from provd.util import format_mac, norm_mac
from twisted.internet import defer

logger = logging.getLogger('plugin.wazo-technicolor')


class BaseTechnicolorHTTPDeviceInfoExtractor:
    _UA_REGEX = re.compile(r'^(?:Thomson|THOMSON) (\w+) hw[^ ]+ fw([^ ]+) ([^ ]+)$')

    def extract(self, request: Request, request_type: RequestType):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request: Request):
        ua = request.getHeader(b'User-Agent')
        if ua:
            # All information is present in the User-Agent header for
            # Technicolor
            return self._extract_info_from_ua(ua.decode('ascii'))
        return None

    def _extract_info_from_ua(self, ua: str):
        # HTTP User-Agent:
        #   "THOMSON ST2022 hw2 fw3.54 00-18-F6-B5-00-00" (from web)
        #   "THOMSON ST2022 hw2 fw4.68 00-14-7F-E1-FC-6D" (from web)
        #   "THOMSON ST2030 hw5 fw2.72 00-14-7F-E1-47-B3"
        #   "THOMSON ST2030 hw5 fw2.74 00-14-7F-E1-47-B3"
        #   "Thomson TB30 hw1 fw1.72.0 00-1F-9F-84-F1-80"
        #   "Thomson TB30 hw1 fw1.74.0 00-1F-9F-84-F1-80"
        m = self._UA_REGEX.match(ua)
        if m:
            raw_model, raw_version, raw_mac = m.groups()
            try:
                mac = norm_mac(raw_mac)
            except ValueError as e:
                logger.warning('Could not normalize MAC address "%s": %s', raw_mac, e)
                return None
            return {
                'vendor': 'Technicolor',
                'model': raw_model,
                'version': raw_version,
                'mac': mac,
            }
        return None


class BaseTechnicolorPgAssociator(BasePgAssociator):
    def __init__(self, model, version):
        super().__init__()
        self._model = model
        self._version = version

    def _do_associate(
        self, vendor: str, model: str | None, version: str | None
    ) -> DeviceSupport:
        if vendor == 'Technicolor':
            if model == self._model:
                if version == self._version:
                    return DeviceSupport.EXACT
                return DeviceSupport.COMPLETE
            return DeviceSupport.PROBABLE
        return DeviceSupport.IMPROBABLE


_ZONE_LIST = [
    'Pacific/Kwajalein',  # Eniwetok, Kwajalein
    'Pacific/Midway',  # Midway Island, Samoa
    'US/Hawaii',  # Hawaii
    'US/Alaska',  # Alaska
    'US/Pacific',  # Pacific Time(US & Canada); Tijuana
    'US/Arizona',  # Arizona
    'US/Mountain',  # Mountain Time(US & Canada)
    'US/Central',  # Central Time(US & Canada)
    'America/Tegucigalpa',  # Mexico City, Tegucigalpa (!)
    'Canada/Saskatchewan',  # Central America, Mexico City,Saskatchewan (!)
    'America/Bogota',  # Bogota, Lima, Quito
    'US/Eastern',  # Eastern Time(US & Canada)
    'US/East-Indiana',  # Indiana(East)
    'Canada/Atlantic',  # Atlantic Time (Canada)
    'America/La_Paz',  # Caracas, La Paz
    'Canada/Newfoundland',  # Newfoundland
    'America/Sao_Paulo',  # Brasilia
    'America/Argentina/Buenos_Aires',  # Buenos Aires, Georgetown
    'Atlantic/South_Georgia',  # Mid-Atlantic
    'Atlantic/Azores',  # Azores, Cape Verde Is
    'Africa/Casablanca',  # Casablanca, Monrovia    (!)
    'Europe/London',  # Greenwich Mean Time: Dublin, Edinburgh, Lisbon, London
    'Europe/Paris',  # Amsterdam, Copenhagen, Madrid, Paris, Vilnius
    'Europe/Belgrade',  # Central Europe Time(Belgrade, Sarajevo, Skopje, Sofija, Zagreb) (?)
    'Europe/Bratislava',  # Bratislava, Budapest, Ljubljana, Prague, Warsaw
    'Europe/Brussels',  # Brussels, Berlin, Bern, Rome, Stockholm, Vienna
    'Europe/Athens',  # Athens, Istanbul, Minsk
    'Europe/Bucharest',  # Bucharest
    'Africa/Cairo',  # Cairo
    'Africa/Harare',  # Harare, Pretoria
    'Europe/Helsinki',  # Helsinki, Riga, Tallinn
    'Israel',  # Israel
    'Asia/Baghdad',  # Baghdad, Kuwait, Riyadh
    'Europe/Moscow',  # Moscow, St. Petersburg, Volgograd
    'Africa/Nairobi',  # Nairobi
    'Asia/Tehran',  # Tehran
    'Asia/Muscat',  # Abu Dhabi, Muscat
    'Asia/Baku',  # Baku, Tbilisi (!)
    'Asia/Kabul',  # Kabul
    'Asia/Yekaterinburg',  # Ekaterinburg
    'Asia/Karachi',  # Islamabad, Karachi, Tashkent
    'Asia/Calcutta',  # Bombay, Calcutta, Madras, New Delhi
    'Asia/Kathmandu',  # Kathmandu
    'Asia/Almaty',  # Almaty, Dhaka
    'Asia/Colombo',  # Colombo
    'Asia/Rangoon',  # Rangoon
    'Asia/Bangkok',  # Bangkok, Hanoi, Jakarta
    'Asia/Hong_Kong',  # Beijin, Chongqing, Hong Kong, Urumqi
    'Australia/Perth',  # Perth
    'Asia/Urumqi',  # Urumqi,Taipei, Kuala Lumpur, Sinapore
    'Asia/Tokyo',  # Osaka, Sappora, Tokyo
    'Asia/Seoul',  # Seoul
    'Asia/Yakutsk',  # Yakutsk
    'Australia/Adelaide',  # Adelaide
    'Australia/Darwin',  # Darwin
    'Australia/Brisbane',  # Brisbane
    'Australia/Canberra',  # Canberra, Melbourne, Sydney
    'Pacific/Guam',  # Guam, Port Moresby
    'Australia/Hobart',  # Hobart
    'Asia/Vladivostok',  # Vladivostok
    'Asia/Magadan',  # Magadan, Solomon Is., New Caledonia
    'Pacific/Auckland',  # Auckland, Wellington
    'Pacific/Fiji',  # Fiji, Kamchatka, Marshall Is. (!)
    'Pacific/Tongatapu',  # Nuku'alofa
]


def _gen_tz_map():
    result = {}
    for i, tz_name in enumerate(_ZONE_LIST):
        inform = tzinform.get_timezone_info(tz_name)
        inner_dict = result.setdefault(inform['utcoffset'].as_minutes, {})
        if not inform['dst']:
            inner_dict[None] = i
        else:
            inner_dict[inform['dst']['as_string']] = i
    return result


class BaseTechnicolorPlugin(StandardPlugin):
    _ENCODING = 'ISO-8859-1'
    _TZ_MAP = _gen_tz_map()
    _LOCALE = {
        # <locale id>, (<langage type>, <country code>)
        'de_DE': ('3', 'DE'),
        'en_US': ('0', 'US'),
        'es_ES': ('2', 'ES'),
        'fr_FR': ('1', 'FR'),
        'fr_CA': ('1', 'US'),
    }
    _LOCALE_DEF = ('0', 'US')
    _SIP_DTMF_MODE = {'RTP-in-band': '0', 'RTP-out-of-band': '1', 'SIP-INFO': '4'}
    _DTMF_DEF = '1'
    _SIP_TRANSPORT = {'udp': '0', 'tcp': '1', 'tls': '2'}
    _TRANSPORT_DEF = '0'
    _NTP_ZONE_NUM_DEF = '23'
    _XX_PHONEBOOK_NAME = {'fr': 'Annuaire entreprise', 'en': 'Enterprise directory'}
    _XX_PHONEBOOK_NAME_DEF = ''
    _NB_FKEYS = 66
    _NB_LINES = 4

    def __init__(self, app, plugin_dir, gen_cfg, spec_cfg):
        super().__init__(app, plugin_dir, gen_cfg, spec_cfg)

        self._tpl_helper = TemplatePluginHelper(plugin_dir)

        downloaders = FetchfwPluginHelper.new_downloaders(gen_cfg.get('proxies'))
        fetchfw_helper = FetchfwPluginHelper(plugin_dir, downloaders)

        self.services = fetchfw_helper.services()
        self.http_service = HTTPNoListingFileService(self._tftpboot_dir)

    http_dev_info_extractor = BaseTechnicolorHTTPDeviceInfoExtractor()

    def configure_common(self, raw_config):
        self._add_server_url(raw_config)
        for tpl_filename, filename in self._COMMON_TEMPLATES:
            tpl = self._tpl_helper.get_template(tpl_filename)
            dst = os.path.join(self._tftpboot_dir, filename)
            self._tpl_helper.dump(tpl, raw_config, dst, self._ENCODING)

    def _add_country_and_lang(self, raw_config):
        locale = raw_config.get('locale')
        (
            raw_config['XX_language_type'],
            raw_config['XX_country_code'],
        ) = self._LOCALE.get(locale, self._LOCALE_DEF)

    def _add_config_sn(self, raw_config):
        # The only thing config_sn needs to be is 12 digit long and different
        # from one config file to another.
        raw_config['XX_config_sn'] = f'{time.time():012f}'

    def _add_dtmf_mode_flag(self, raw_config):
        dtmf_mode = raw_config.get('sip_dtmf_mode')
        raw_config['XX_dtmf_mode_flag'] = self._SIP_DTMF_MODE.get(
            dtmf_mode, self._DTMF_DEF
        )

    def _add_transport_flg(self, raw_config):
        sip_transport = raw_config.get('sip_transport')
        raw_config['XX_transport_flg'] = self._SIP_TRANSPORT.get(
            sip_transport, self._TRANSPORT_DEF
        )

    def _gen_xx_phonebook_name(self, raw_config):
        if 'locale' in raw_config:
            language = raw_config['locale'].split('_')[0]
            return self._XX_PHONEBOOK_NAME.get(language, self._XX_PHONEBOOK_NAME_DEF)
        return self._XX_PHONEBOOK_NAME_DEF

    def _tzinfo_to_zone_num(self, tzinfo):
        utcoffset_m = tzinfo['utcoffset'].as_minutes
        if utcoffset_m not in self._TZ_MAP:
            # No UTC offset matching. Let's try finding one relatively close...
            for supp_offset in [30, -30, 60, -60]:
                if utcoffset_m + supp_offset in self._TZ_MAP:
                    utcoffset_m += supp_offset
                    break
            else:
                return self._XX_NTP_ZONE_NUM_DEF

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
                dst_key = dst_map.keys[0]
        return dst_map[dst_key]

    def _add_ntp_zone_num(self, raw_config):
        raw_config['XX_ntp_zone_num'] = self._NTP_ZONE_NUM_DEF
        if 'timezone' in raw_config:
            try:
                tzinfo = tzinform.get_timezone_info(raw_config['timezone'])
            except tzinform.TimezoneNotFoundError as e:
                logger.info('Unknown timezone: %s', e)
            else:
                raw_config['XX_ntp_zone_num'] = self._tzinfo_to_zone_num(tzinfo)

    def _add_fkeys(self, raw_config):
        funckeys = raw_config['funckeys']
        lines = []
        for keynum in range(1, self._NB_FKEYS + 1):
            funckey_no = str(keynum)
            if funckey_no in funckeys:
                funckey_dict = funckeys[funckey_no]
                funckey_type = funckey_dict['type']
                if funckey_type == 'speeddial':
                    prefix = 'L'
                elif funckey_type == 'blf':
                    prefix = 'S'
                else:
                    logger.info('Unsupported funckey type: %s', funckey_type)
                    lines.append(f'FeatureKeyExt{keynum:02d}=L/<sip:>')
                    continue
                lines.append(
                    'FeatureKeyExt%02d=%s/<sip:%s>'
                    % (keynum, prefix, funckey_dict['value'])
                )
            else:
                lines.append(f'FeatureKeyExt{keynum:02d}=L/<sip:>')
        raw_config['XX_fkeys'] = '\n'.join(lines)

    def _add_xivo_phonebook_url(self, raw_config):
        plugins.add_xivo_phonebook_url(
            raw_config, 'thomson', entry_point='lookup', qs_suffix='term=#SEARCH'
        )

    def _add_server_url(self, raw_config):
        if raw_config.get('http_base_url'):
            _, _, remaining_url = raw_config['http_base_url'].partition('://')
            raw_config['XX_server_url'] = raw_config['http_base_url']
            raw_config['XX_server_url_without_scheme'] = remaining_url
        else:
            base_url = f"{raw_config['ip']}:{raw_config['http_port']}"
            raw_config['XX_server_url_without_scheme'] = base_url
            raw_config['XX_server_url'] = f"http://{base_url}"

    def _dev_specific_filename(self, device: dict[str, str]) -> str:
        # Return the device specific filename (not pathname) of device
        formatted_mac = format_mac(device['mac'], separator='', uppercase=True)
        return f'{self._FILENAME_PREFIX}_{formatted_mac}.txt'

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

        self._add_country_and_lang(raw_config)
        self._add_config_sn(raw_config)
        self._add_dtmf_mode_flag(raw_config)
        self._add_transport_flg(raw_config)
        self._add_ntp_zone_num(raw_config)
        self._add_fkeys(raw_config)
        self._add_xivo_phonebook_url(raw_config)
        self._add_server_url(raw_config)
        raw_config['XX_phonebook_name'] = self._gen_xx_phonebook_name(raw_config)
        raw_config['XX_nb_lines'] = self._NB_LINES

        path = os.path.join(self._tftpboot_dir, filename)
        self._tpl_helper.dump(tpl, raw_config, path, self._ENCODING, errors='replace')

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
