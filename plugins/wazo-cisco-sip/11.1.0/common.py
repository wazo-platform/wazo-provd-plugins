# Copyright 2010-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+
from __future__ import annotations

import logging
import os
import re
from operator import itemgetter
from xml.sax.saxutils import escape
from provd import plugins
from provd import tzinform
from provd import synchronize
from provd.devices.config import RawConfigError
from provd.devices.pgasso import BasePgAssociator, DeviceSupport
from provd.plugins import StandardPlugin, TemplatePluginHelper, FetchfwPluginHelper
from provd.servers.http import HTTPNoListingFileService
from provd.servers.http_site import Request
from provd.servers.tftp.service import TFTPFileService
from provd.util import norm_mac, format_mac
from provd.devices.ident import RequestType, DHCPRequest
from provd.servers.tftp.packet import Packet
from provd.servers.tftp.service import TFTPRequest
from twisted.internet import defer

logger = logging.getLogger('plugins.wazo-cisco-sip')


def _norm_model(raw_model: str) -> str:
    # Normalize a model name and return it as a unicode string. This removes
    # minus sign and make all the characters uppercase.
    return raw_model.replace('-', '').upper()


class BaseCiscoDHCPDeviceInfoExtractor:
    _CISCO_VDI_REGEX = re.compile(r'^CISCO (ATA[0-9]{3})-MPP')

    def extract(self, request: DHCPRequest, request_type: RequestType):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request: DHCPRequest):
        options: dict = request['options']
        logger.debug('_do_extract request: %s', request)
        if 60 in options:
            return self._extract_from_vdi(options[60])
        return None

    def _extract_from_vdi(self, vdi: str):
        # Vendor class identifier:
        # CISCO ATA191-MPP
        # CISCO ATA192-MPP

        m = self._CISCO_VDI_REGEX.match(vdi)
        if m:
            model = m.group(1)
            return {'vendor': 'Cisco', 'model': _norm_model(model)}
        return None


class BaseCiscoHTTPDeviceInfoExtractor:
    _CISCO_UA_REGEX = re.compile(r'^Cisco/(ATA[0-9]{3})-MPP-(\S+) \((\S+)\)$')
    _PATH_REGEX = re.compile(r'\b/([\da-f]{12})\.xml$')

    def extract(self, request: Request, request_type: RequestType):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request: Request):
        ua = request.getHeader(b'User-Agent')
        raw_mac = request.args.get(b'mac', [None])[0]
        dev_info = {}
        if raw_mac:
            dev_info['mac'] = norm_mac(raw_mac.decode('ascii'))
            logger.debug('Got MAC from URL: %s', dev_info['mac'])
        if ua:
            self._extract_from_ua(ua.decode('ascii'), dev_info)
            if dev_info:
                dev_info['vendor'] = 'Cisco'
                if 'mac' not in dev_info or 'model' not in dev_info:
                    self._extract_from_path(request.path.decode('ascii'), dev_info)
                return dev_info
        return None

    def _extract_from_ua(self, ua: str, dev_info: dict[str, str]):
        # HTTP User-Agent:
        # Note: the last group of digit is the serial number
        #   It is not possible to extract the MAC address from the UA on these ATAs
        #   Cisco/ATA191-MPP-11-1-0-MSR4 (FCH2443D9R4)
        m = self._CISCO_UA_REGEX.match(ua)
        if m:
            model, version, dev_sn = m.groups()
            dev_info['model'] = model
            dev_info['version'] = version
            if dev_sn:
                dev_info['sn'] = dev_sn

    def _extract_from_path(self, path: str, dev_info: dict[str, str]):
        # try to extract MAC address from path
        m = self._PATH_REGEX.search(path)
        if m:
            raw_mac = m.group(1)
            try:
                dev_info['mac'] = norm_mac(raw_mac)
            except ValueError as e:
                logger.warning('Could not normalize MAC address: %s', e)


class BaseCiscoTFTPDeviceInfoExtractor:
    _MACFILE_REGEX = re.compile(r'^/([\da-fA-F]{12})\.xml$')

    def extract(self, request: TFTPRequest, request_type: RequestType):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request: TFTPRequest):
        packet: Packet = request['packet']
        filename = packet['filename'].decode('ascii')
        dev_info = self._test_macfile(filename)
        if dev_info:
            dev_info['vendor'] = 'Cisco'
            return dev_info
        return None

    def _test_macfile(self, filename: str):
        # Test if filename is "/$MA.xml".
        m = self._MACFILE_REGEX.match(filename)
        if m:
            raw_mac = m.group(1)
            try:
                mac = norm_mac(raw_mac)
            except ValueError as e:
                logger.warning('Could not normalize MAC address: %s', e)
                return None
            return {'mac': mac}
        return None


class BaseCiscoPgAssociator(BasePgAssociator):
    def __init__(self, model_version):
        super().__init__()
        self._model_version = model_version

    def _do_associate(
        self, vendor: str, model: str | None, version: str | None
    ) -> DeviceSupport:
        if vendor == 'Cisco':
            if model in self._model_version:
                if version == self._model_version[model]:
                    return DeviceSupport.EXACT
                return DeviceSupport.COMPLETE
            if model is not None:
                # model is unknown to the plugin, chance are low
                # that it's going to be supported because of missing
                # common configuration file that are used to bootstrap
                # the provisioning process
                return DeviceSupport.IMPROBABLE
            return DeviceSupport.PROBABLE
        return DeviceSupport.IMPROBABLE


class BaseCiscoSipPlugin(StandardPlugin):
    """Base classes MUST have a '_COMMON_FILENAMES' attribute which is a
    sequence of filenames that will be generated by the common template in
    the common_configure function.

    """

    _ENCODING = 'UTF-8'
    _NB_FKEY = {
        # <model>: (<nb keys>, <nb expansion modules>)
        'ATA191': (0, 0),
        'ATA192': (0, 0),
    }
    _DEFAULT_LOCALE = 'en_US'
    _LANGUAGE = {
        'de_DE': 'German',
        'en_US': 'English',
        'es_ES': 'Spanish',
        'fr_FR': 'French',
        'fr_CA': 'French',
    }
    _LOCALE = {
        'de_DE': 'de-DE',
        'en_US': 'en-US',
        'es_ES': 'es-ES',
        'fr_FR': 'fr-FR',
        'fr_CA': 'fr-CA',
    }
    _DIRECTORY_NAME = {
        'en_US': 'Wazo Directory',
        'fr_FR': 'Répertoire Wazo',
    }

    def __init__(self, app, plugin_dir, gen_cfg, spec_cfg):
        super().__init__(app, plugin_dir, gen_cfg, spec_cfg)

        downloaders = FetchfwPluginHelper.new_downloaders(gen_cfg.get('proxies'))
        fetchfw_helper = FetchfwPluginHelper(plugin_dir, downloaders)

        self.services = fetchfw_helper.services()

        self._tpl_helper = TemplatePluginHelper(plugin_dir)

        self.http_service = HTTPNoListingFileService(self._tftpboot_dir)
        self.tftp_service = TFTPFileService(self._tftpboot_dir)

    dhcp_dev_info_extractor = BaseCiscoDHCPDeviceInfoExtractor()

    http_dev_info_extractor = BaseCiscoHTTPDeviceInfoExtractor()

    tftp_dev_info_extractor = BaseCiscoTFTPDeviceInfoExtractor()

    _SENSITIVE_FILENAME_REGEX = re.compile(r'^\w{,3}[0-9a-fA-F]{12}(?:\.cnf)?\.xml$')

    def configure_common(self, raw_config):
        tpl = self._tpl_helper.get_template('common/model.cfg.tpl')
        common_filenames = self._COMMON_FILENAMES
        for filename in common_filenames:
            dst = os.path.join(self._tftpboot_dir, filename)
            self._tpl_helper.dump(tpl, raw_config, dst, self._ENCODING)

    def _add_fkeys(self, raw_config, model):
        if model not in self._NB_FKEY:
            logger.info('Unknown model or model with no funckeys: %s', model)
            return
        nb_keys, nb_expmods = self._NB_FKEY[model]
        lines = []
        for funckey_no, funckey_dict in sorted(
            iter(raw_config['funckeys'].items()), key=itemgetter(0)
        ):
            funckey_type = funckey_dict['type']
            value = funckey_dict['value']
            label = escape(funckey_dict.get('label', value))
            if funckey_type == 'speeddial':
                function = f'fnc=sd;ext={value}@$PROXY;nme={label}'
            elif funckey_type == 'blf':
                function = f'fnc=sd+blf+cp;sub={value}@$PROXY;nme={label}'
            else:
                logger.info('Unsupported funckey type: %s', funckey_type)
                continue
            keynum = int(funckey_no)
            if keynum <= nb_keys:
                lines += [
                    f'<Extension_{funckey_no}_>Disabled</Extension_{funckey_no}_>',
                    f'<Short_Name_{funckey_no}_>{label}</Short_Name_{funckey_no}_>',
                    f'<Extended_Function_{funckey_no}_>{function}</Extended_Function_{funckey_no}_>',  # noqa: E501
                ]
            else:
                expmod_keynum = keynum - nb_keys - 1
                expmod_no = expmod_keynum // 32 + 1
                if expmod_no > nb_expmods:
                    logger.info(
                        'Model %s has less than %s function keys', model, funckey_no
                    )
                else:
                    expmod_key_no = expmod_keynum % 32 + 1
                    lines.append(
                        f'<Unit_{expmod_no}_Key_{expmod_key_no}>'
                        f'{function}'
                        f'</Unit_{expmod_no}_Key_{expmod_key_no}>'
                    )
        raw_config['XX_fkeys'] = '\n'.join(lines)

    def _format_dst_change(self, dst_change):
        _day = dst_change['day']
        if _day.startswith('D'):
            day = _day[1:]
            weekday = '0'
        else:
            week, weekday = _day[1:].split('.')
            weekday = tzinform.week_start_on_monday(int(weekday))
            if week == '5':
                day = '-1'
            else:
                day = (int(week) - 1) * 7 + 1

        h, m, s = dst_change['time'].as_hms
        return f'{dst_change["month"]}/{day}/{weekday}/{h}:{m}:{s}'

    def _format_tzinfo(self, tzinfo):
        lines = []
        hours, minutes = tzinfo['utcoffset'].as_hms[:2]
        lines.append(f'<Time_Zone>GMT{hours:+03d}:{minutes:02d}</Time_Zone>')
        if tzinfo['dst'] is None:
            lines.append(
                '<Daylight_Saving_Time_Enable>no</Daylight_Saving_Time_Enable>'
            )
        else:
            lines.append(
                '<Daylight_Saving_Time_Enable>yes</Daylight_Saving_Time_Enable>'
            )
            h, m, s = tzinfo['dst']['save'].as_hms
            start = self._format_dst_change(tzinfo['dst']['start'])
            end = self._format_dst_change(tzinfo['dst']['end'])
            lines.append(
                '<Daylight_Saving_Time_Rule>'
                f'start={start};end={end};save={h:d}:{m:d}:{s}'
                '</Daylight_Saving_Time_Rule>'
            )
        return '\n'.join(lines)

    def _add_timezone(self, raw_config):
        if 'timezone' in raw_config:
            try:
                tzinfo = tzinform.get_timezone_info(raw_config['timezone'])
            except tzinform.TimezoneNotFoundError as e:
                logger.info('Unknown timezone: %s', e)
            else:
                raw_config['XX_timezone'] = self._format_tzinfo(tzinfo)

    def _format_proxy(self, raw_config, line, line_no):
        proxy_ip = line.get('proxy_ip') or raw_config['sip_proxy_ip']
        backup_proxy_ip = line.get('backup_proxy_ip') or raw_config.get(
            'sip_backup_proxy_ip'
        )
        proxy_port = line.get('proxy_port') or raw_config.get('sip_proxy_port', '5060')
        backup_proxy_port = line.get('backup_proxy_port') or raw_config.get(
            'sip_backup_proxy_port', '5060'
        )
        if backup_proxy_ip:
            proxy_value = (
                f'xivo_proxies{line_no}:SRV={proxy_ip}:{proxy_port}:p=0|'
                f'{backup_proxy_ip}:{backup_proxy_port}:p=1'
            )
        else:
            proxy_value = f'{proxy_ip}:{proxy_port}'
        return proxy_value

    def _add_proxies(self, raw_config):
        proxies = {}
        for line_no, line in raw_config['sip_lines'].items():
            proxies[line_no] = self._format_proxy(raw_config, line, line_no)
        raw_config['XX_proxies'] = proxies

    def _add_language(self, raw_config):
        locale = raw_config.get('locale')
        if locale in self._LANGUAGE:
            raw_config['XX_language'] = self._LANGUAGE[locale]

    def _add_directory_name(self, raw_config):
        locale = raw_config.get('locale')
        if locale not in self._DIRECTORY_NAME:
            locale = self._DEFAULT_LOCALE
        raw_config['XX_directory_name'] = self._DIRECTORY_NAME[locale]

    def _add_locale(self, raw_config):
        locale = raw_config.get('locale')
        if locale not in self._LOCALE:
            locale = self._DEFAULT_LOCALE
        raw_config['XX_locale'] = self._LOCALE[locale]

    def _add_xivo_phonebook_url(self, raw_config):
        plugins.add_xivo_phonebook_url(raw_config, 'cisco')

    def _dev_specific_filename(self, dev):
        # Return the device specific filename (not pathname) of device
        formatted_mac = format_mac(dev['mac'], separator='')
        return formatted_mac + '.xml'

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

        self._add_fkeys(raw_config, device.get('model'))
        self._add_timezone(raw_config)
        self._add_proxies(raw_config)
        self._add_language(raw_config)
        self._add_directory_name(raw_config)
        self._add_locale(raw_config)
        self._add_xivo_phonebook_url(raw_config)

        path = os.path.join(self._tftpboot_dir, filename)
        self._tpl_helper.dump(tpl, raw_config, path, self._ENCODING, errors='replace')

    def deconfigure(self, device):
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

    def is_sensitive_filename(self, filename):
        return bool(self._SENSITIVE_FILENAME_REGEX.match(filename))
