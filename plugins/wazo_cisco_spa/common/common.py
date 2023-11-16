# Copyright 2010-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import logging
import os
import re
from copy import deepcopy
from operator import itemgetter
from xml.sax.saxutils import escape
from provd import plugins
from provd import tzinform
from provd import synchronize
from provd.devices.config import RawConfigError
from provd.devices.pgasso import BasePgAssociator, DeviceSupport
from provd.plugins import StandardPlugin, FetchfwPluginHelper, TemplatePluginHelper
from provd.servers.http import HTTPNoListingFileService
from provd.servers.tftp.service import TFTPFileService
from provd.util import norm_mac, format_mac
from provd.servers.http_site import Request
from provd.devices.ident import RequestType, DHCPRequest
from provd.servers.tftp.packet import Packet
from provd.servers.tftp.service import TFTPRequest
from twisted.internet import defer

logger = logging.getLogger('plugins.wazo-cisco-spa')


def _norm_model(raw_model: str) -> str:
    # Normalize a model name and return it as a unicode string. This removes
    # minus sign and make all the characters uppercase.
    return raw_model.replace('-', '').upper()


class BaseCiscoDHCPDeviceInfoExtractor:
    _RAW_VENDORS = ['linksys', 'cisco']
    _CISCO_VDI_REGEX = re.compile(r'^(CISCO|Cisco) (SPA[0-9]{3}|ATA190G?g?2?)')
    _LINKSYS_VDI_REGEX = re.compile(r'^(LINKSYS) (SPA-?[0-9]{3,4})')
    _VDIS = [_CISCO_VDI_REGEX, _LINKSYS_VDI_REGEX]

    def extract(self, request: DHCPRequest, request_type: RequestType):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request: DHCPRequest):
        options = request['options']
        logger.debug('_do_extract request: %s', request)
        if 60 in options:
            return self._extract_from_vdi(options[60])
        return None

    def _extract_from_vdi(self, vdi):
        # Vendor class identifier:
        #   "LINKSYS SPA-942" (SPA942 6.1.5a)
        #   "LINKSYS SPA-962" (SPA962 6.1.5a)
        #   "LINKSYS SPA8000" (SPA8000 unknown version)
        #   "Cisco SPA501G" (SPA501G 7.4.4)
        #   "Cisco SPA508G" (SPA508G 7.4.4)
        #   "Cisco SPA525g" (SPA525G unknown version, from Cisco documentation)
        #   "Cisco SPA525G" (SPA525G 7.4.4)
        #   "Cisco SPA525G" (SPA525G 7.4.7)
        #   "Cisco SPA525G2" (SPA525G2 7.4.5)
        #   "CISCO SPA122"
        #   "CISCO ATA190"

        for vdi_matcher in self._VDIS:
            match = vdi_matcher.match(vdi)
            if match:
                raw_vendor, raw_model = match.groups()
                if raw_vendor.lower() in self._RAW_VENDORS:
                    dev_info = {'vendor': 'Cisco', 'model': _norm_model(raw_model)}
                    return dev_info
        return None


class BaseCiscoHTTPDeviceInfoExtractor:
    _LINKSYS_UA_REGEX = re.compile(r'^Linksys/([\w\-]+)-([^\s\-]+) \((\w+)\)$')
    _CISCO_UA_REGEX = re.compile(r'^Cisco/(\w+)-(\S+) (?:\(([\dA-F]{12})\))?\((\w+)\)$')
    _PATH_REGEX = re.compile(r'\b([\da-f]{12})\.xml$')

    def extract(self, request: Request, request_type: RequestType):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request: Request):
        ua = request.getHeader(b'User-Agent')
        if ua:
            dev_info = {}
            self._extract_from_ua(ua.decode('ascii'), dev_info)
            if dev_info:
                dev_info['vendor'] = 'Cisco'
                if 'mac' not in dev_info:
                    self._extract_from_path(request.path.decode('ascii'), dev_info)
                return dev_info
        return None

    def _extract_from_ua(self, ua: str, dev_info: dict[str, str]):
        # HTTP User-Agent:
        # Note: the last group of digit is the serial number;
        #       the first, if present, is the MAC address
        #   "Linksys/SPA-942-6.1.5(a) (88019FA42805)"
        #   "Linksys/SPA-962-6.1.5(a) (4MM00F903042)"
        #   "Cisco/SPA501G-7.4.4 (8843E157DDCC)(CBT141100HR)"
        #   "Cisco/SPA508G-7.4.4 (0002FDFF2103)(CBT141400UK)"
        #   "Cisco/SPA508G-7.4.8a (0002FDFF2103)(CBT141400UK)"
        #   "Cisco/SPA525G-7.4.4 (CBT141900G7)"
        #   "Cisco/SPA525G-7.4.7 (CBT141900G7)"
        if ua.startswith('Linksys/'):
            self._extract_linksys_from_ua(ua, dev_info)
        elif ua.startswith('Cisco/'):
            self._extract_cisco_from_ua(ua, dev_info)

    def _extract_linksys_from_ua(self, ua: str, dev_info: dict[str, str]):
        # Pre: ua.startswith('Linksys/')
        m = self._LINKSYS_UA_REGEX.match(ua)
        if m:
            raw_model, version, sn = m.groups()
            dev_info['model'] = _norm_model(raw_model)
            dev_info['version'] = version
            dev_info['sn'] = sn

    def _extract_cisco_from_ua(self, ua: str, dev_info: dict[str, str]):
        # Pre: ua.startswith('Cisco/')
        m = self._CISCO_UA_REGEX.match(ua)
        if m:
            model, version, raw_mac, sn = m.groups()
            dev_info['model'] = model
            dev_info['version'] = version
            if raw_mac:
                dev_info['mac'] = norm_mac(raw_mac)
            dev_info['sn'] = sn

    def _extract_from_path(self, path: str, dev_info: dict[str, str]):
        # try to extract MAC address from path
        m = self._PATH_REGEX.search(path)
        if m:
            raw_mac = m.group(1)
            try:
                mac = norm_mac(raw_mac)
            except ValueError as e:
                logger.warning('Could not normalize MAC address: %s', e)
            else:
                dev_info['mac'] = mac


class BaseCiscoTFTPDeviceInfoExtractor:
    _SEPFILE_REGEX = re.compile(r'^SEP([\dA-F]{12})\.cnf\.xml$')
    _SPAFILE_REGEX = re.compile(r'^/spa(.+?)\.cfg$')
    _ATAFILE_REGEX = re.compile(r'^ATA([\dA-F]{12})\.cnf\.xml$')
    _CTLSEPFILE_REGEX = re.compile(r'^CTLSEP([\dA-F]{12})\.tlv$')

    def extract(self, request: TFTPRequest, request_type: RequestType):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request: TFTPRequest):
        packet: Packet = request['packet']
        filename = packet['filename'].decode('ascii')
        for test_fun in [self._test_spafile, self._test_init, self._test_atafile]:
            dev_info = test_fun(filename)
            if dev_info:
                dev_info['vendor'] = 'Cisco'
                return dev_info
        return None

    def __repr__(self):
        return object.__repr__(self) + "-SPA"

    def _test_spafile(self, filename: str):
        # Test if filename is "/spa$PSN.cfg".
        m = self._SPAFILE_REGEX.match(filename)
        if m:
            raw_model = 'SPA' + m.group(1)
            return {'model': _norm_model(raw_model)}
        return None

    def _test_atafile(self, filename: str):
        # Test if filename is "ATAMAC.cnf.xml".
        # Only the ATA190 requests this file
        m = self._ATAFILE_REGEX.match(filename)
        if m:
            return {'model': 'ATA190'}
        return None

    def _test_init(self, filename: str):
        # Test if filename is "/init.cfg".
        if filename == '/init.cfg':
            return {'model': 'PAP2T'}
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
                # then it's going to be supported because of missing
                # common configuration file that are used to bootstrap
                # the provisioning process
                return DeviceSupport.IMPROBABLE
            return DeviceSupport.PROBABLE
        return DeviceSupport.IMPROBABLE


class BaseCiscoPlugin(StandardPlugin):
    """Base classes MUST have a '_COMMON_FILENAMES' attribute which is a
    sequence of filenames that will be generated by the common template in
    the common_configure function.

    """

    _ENCODING = 'UTF-8'
    _NB_FKEY = {
        # <model>: (<nb keys>, <nb expansion modules>)
        'SPA941': (4, 0),
        'SPA942': (4, 0),
        'SPA962': (6, 2),
        'SPA303': (3, 2),
        'SPA501G': (8, 2),
        'SPA502G': (0, 2),
        'SPA504G': (4, 2),
        'SPA508G': (8, 2),
        'SPA509G': (12, 2),
        'SPA512G': (0, 2),
        'SPA514G': (4, 2),
        'SPA525G': (5, 2),
        'SPA525G2': (5, 2),
        'ATA190': (0, 0),
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
    _SENSITIVE_FILENAME_REGEX = re.compile(r'^\w{,3}[0-9a-fA-F]{12}(?:\.cnf)?\.xml$')

    def __init__(self, app, plugin_dir, gen_cfg, spec_cfg):
        super().__init__(app, plugin_dir, gen_cfg, spec_cfg)

        self._tpl_helper = TemplatePluginHelper(plugin_dir)

        downloaders = FetchfwPluginHelper.new_downloaders(gen_cfg.get('proxies'))
        fetchfw_helper = FetchfwPluginHelper(plugin_dir, downloaders)
        self.services = fetchfw_helper.services()

        self.http_service = HTTPNoListingFileService(self._tftpboot_dir)
        self.tftp_service = TFTPFileService(self._tftpboot_dir)

    dhcp_dev_info_extractor = BaseCiscoDHCPDeviceInfoExtractor()

    http_dev_info_extractor = BaseCiscoHTTPDeviceInfoExtractor()

    tftp_dev_info_extractor = BaseCiscoTFTPDeviceInfoExtractor()

    def configure_common(self, raw_config):
        self._add_server_url(raw_config)
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
                    f'<Extended_Function_{funckey_no}_>'
                    f'{function}</Extended_Function_{funckey_no}_>',
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
                        f'{function}</Unit_{expmod_no}_Key_{expmod_key_no}>'
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
                f'<Daylight_Saving_Time_Rule>'
                f'start={start};end={end};save={h:d}:{m:d}:{s}'
                f'</Daylight_Saving_Time_Rule>'
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

    def _add_server_url(self, raw_config):
        if 'http_base_url' in raw_config:
            _, _, remaining_url = raw_config['http_base_url'].partition('://')
            raw_config['XX_server_url'] = raw_config['http_base_url']
            raw_config['XX_server_url_without_scheme'] = remaining_url
        else:
            base_url = f"{raw_config['ip']}:{raw_config['http_port']}"
            raw_config['XX_server_url_without_scheme'] = base_url
            raw_config['XX_server_url'] = f"http://{base_url}"

    def _dev_specific_filename(self, dev: dict[str, str]) -> str:
        # Return the device specific filename (not pathname) of device
        formatted_mac = format_mac(dev['mac'], separator='')

        if dev.get('model', '').startswith('ATA'):
            formatted_mac = f'ATA{formatted_mac.upper()}.cnf'

        return formatted_mac + '.xml'

    def _dev_shifted_device(self, dev):
        device2 = deepcopy(dev)
        device2['mac'] = device2['mac'][3:] + ':01'
        return device2

    def _dev_shifted_specific_filename(self, dev):
        '''Returns a device specific filename based on the shifted MAC address,
        as required by the Cisco ATA190 for the second phone port.'''
        return self._dev_specific_filename(self._dev_shifted_device(dev))

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
        self._add_server_url(raw_config)

        path = os.path.join(self._tftpboot_dir, filename)
        self._tpl_helper.dump(tpl, raw_config, path, self._ENCODING, errors='replace')

        if len(raw_config['sip_lines']) >= 2 and device.get('model', '').startswith(
            'ATA'
        ):
            raw_config['XX_second_line_ata'] = True

            filename = self._dev_shifted_specific_filename(device)
            path = os.path.join(self._tftpboot_dir, filename)
            self._tpl_helper.dump(
                tpl, raw_config, path, self._ENCODING, errors='replace'
            )

    def deconfigure(self, device):
        path = os.path.join(self._tftpboot_dir, self._dev_specific_filename(device))

        if device.get('model', '').startswith('ATA'):
            path2 = os.path.join(
                self._tftpboot_dir, self._dev_shifted_specific_filename(device)
            )
            try:
                os.remove(path2)
            except OSError as e:
                logger.info('error while removing configuration file: %s', e)
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
