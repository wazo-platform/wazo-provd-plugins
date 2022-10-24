# Copyright 2010-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import os.path
import re
import glob
from operator import itemgetter
from pkg_resources import parse_version
from xml.sax.saxutils import escape
from provd import plugins
from provd import tzinform
from provd import synchronize
from provd.devices.config import RawConfigError
from provd.devices.pgasso import BasePgAssociator, IMPROBABLE_SUPPORT, \
    PROBABLE_SUPPORT, FULL_SUPPORT, NO_SUPPORT, COMPLETE_SUPPORT
from provd.plugins import StandardPlugin, FetchfwPluginHelper, \
    TemplatePluginHelper
from provd.servers.http import HTTPNoListingFileService
from provd.util import norm_mac, format_mac
from twisted.internet import defer, threads

logger = logging.getLogger('plugin.xivo-snom')


class BaseSnomHTTPDeviceInfoExtractor:
    _UA_REGEX = re.compile(r'\bsnom(\w+)-SIP ([\d.]+)')
    _UA_REGEX_MAC = re.compile(r'\bsnom(\w+)-SIP\s([\d.]+)\s(.+)\s(?P<mac>[0-9A-F]+)')
    _PATH_REGEX = re.compile(r'\bsnom\w+-([\dA-F]{12})\.htm$')

    def extract(self, request, request_type):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request):
        device_info = {}
        ua = request.getHeader('User-Agent')
        raw_mac = request.args.get('mac', [None])[0]
        if raw_mac:
            logger.debug('Got MAC from URL: %s', raw_mac)
            device_info['mac'] = norm_mac(raw_mac.decode('ascii'))
        if ua:
            info_from_ua = self._extract_from_ua(ua)
            if info_from_ua:
                device_info.update(info_from_ua)
                self._extract_from_path(request.path, device_info)
        return device_info

    def _extract_from_ua(self, ua):
        # HTTP User-Agent:
        #   "Mozilla/4.0 (compatible; snom lid 3605)" --> Snom 6.5.xx
        #   "Mozilla/4.0 (compatible; snom320-SIP 6.5.20; snom320 jffs2 v3.36; snom320 linux 3.38)"
        #   "Mozilla/4.0 (compatible; snom320-SIP 7.3.30 1.1.3-u)"
        #   "Mozilla/4.0 (compatible; snom320-SIP 8.4.18 1.1.3-s)"
        #   "Mozilla/4.0 (compatible; snom710-SIP 8.7.3.19 1.1.5-IFX-05.01.12)"
        #   "Mozilla/4.0 (compatible; snom710-SIP 8.7.5.35 1.1.5-IFX-05.01.12 000413741767)"
        #   "Mozilla/4.0 (compatible; snom760-SIP 8.7.3.19 2010.06)"
        #   "Mozilla/4.0 (compatible; snom820-SIP 8.4.35 1.1.4-IFX-26.11.09)"
        #   "Mozilla/4.0 (compatible; snom870-SIP 8.4.35 SPEAr300 SNOM 1.4)"
        #   "Mozilla/4.0 (compatible; snomPA1-SIP 8.4.35 1.1.3-s)"
        #   "Mozilla/4.0 (compatible; snomD785-SIP 10.1.33.33 2010.12-00004-g9ba52f5 000413922D24 SXM:0 UXM:0)"
        m = self._UA_REGEX_MAC.search(ua)
        if m:
            raw_model, raw_version, _, raw_mac = m.groups()
            return {'vendor': 'Snom',
                    'model': raw_model.decode('ascii'),
                    'mac': norm_mac(raw_mac.decode('ascii')),
                    'version': raw_version.decode('ascii')}
        # if the complete regex did not match, match a smaller one
        m = self._UA_REGEX.search(ua)
        if m:
            raw_model, raw_version = m.groups()
            return {'vendor': 'Snom',
                    'model': raw_model.decode('ascii'),
                    'version': raw_version.decode('ascii')}
        return None

    def _extract_from_path(self, path, dev_info):
        m = self._PATH_REGEX.search(path)
        if m:
            raw_mac = m.group(1)
            dev_info['mac'] = norm_mac(raw_mac.decode('ascii'))


class BaseSnomPgAssociator(BasePgAssociator):
    def __init__(self, models, version):
        self._models = models
        self._version = version

    def _do_associate(self, vendor, model, version):
        if vendor == 'Snom':
            if version is None:
                # Could be an old version with no XML support
                return PROBABLE_SUPPORT
            assert version is not None
            if self._is_incompatible_version(version):
                return NO_SUPPORT
            if model in self._models:
                if version == self._version:
                    return FULL_SUPPORT
                return COMPLETE_SUPPORT
            return PROBABLE_SUPPORT
        return IMPROBABLE_SUPPORT

    def _is_incompatible_version(self, version):
        try:
            maj_version = parse_version(version)
            if maj_version < parse_version('7.0.0.0'):
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
        'SIP-INFO': 'sip_info_only'
    }
    _SIP_TRANSPORT = {
        'udp': 'udp',
        'tcp': 'tcp',
        'tls': 'tls'
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
        StandardPlugin.__init__(self, app, plugin_dir, gen_cfg, spec_cfg)

        self._tpl_helper = TemplatePluginHelper(plugin_dir)

        downloaders = FetchfwPluginHelper.new_downloaders(gen_cfg.get('proxies'))
        fetchfw_helper = FetchfwPluginHelper(plugin_dir, downloaders)

        self.services = fetchfw_helper.services()
        self.http_service = HTTPNoListingFileService(self._tftpboot_dir)

    http_dev_info_extractor = BaseSnomHTTPDeviceInfoExtractor()

    def _add_uxm_firmware(self, raw_config):
        f = glob.glob(os.path.join(self._tftpboot_dir, 'firmware/snomD7C-*.bin')) + glob.glob(os.path.join(self._tftpboot_dir, 'firmware/snomUXM-*.bin'))
        if f:
            if re.match(r"^.*\/snomUXM-.*.bin$", max(f, key=os.path.getmtime)):
                raw_config['XX_uxm_firmware'] = 'uxm'
            if re.match(r"^.*\/snomD7C-.*.bin$", max(f, key=os.path.getmtime)):
                raw_config['XX_uxm_firmware'] = 'uxmc'

    def _common_templates(self):
        yield 'common/gui_lang.xml.tpl', 'gui_lang.xml'
        yield 'common/web_lang.xml.tpl', 'web_lang.xml'
        for tpl_format, file_format in [('common/snom%s.htm.tpl', 'snom%s.htm'),
                                        ('common/snom%s.xml.tpl', 'snom%s.xml'),
                                        ('common/snom%s-firmware.xml.tpl', 'snom%s-firmware.xml')]:
            for model in self._MODELS:
                yield tpl_format % model, file_format % model

    def configure_common(self, raw_config):
        self._add_uxm_firmware(raw_config)
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

    def _add_fkeys(self, raw_config, model):
        lines = []
        for funckey_no, funckey_dict in sorted(iter(raw_config['funckeys'].items()),
                                               key=itemgetter(0)):
            funckey_type = funckey_dict['type']
            if funckey_type == 'speeddial':
                type_ = 'speed'
                suffix = ''
            elif funckey_type == 'park':
                if model in ['710', '715', '720', '725', '760', 'D765']:
                    type_ = 'orbit'
                    suffix = ''
                else:
                    type_ = 'speed'
                    suffix = ''
            elif funckey_type == 'blf':
                if 'exten_pickup_call' in raw_config:
                    type_ = 'blf'
                    suffix = f'|{raw_config["exten_pickup_call"]}'
                else:
                    logger.warning('Could not set funckey %s: no exten_pickup_call',
                                   funckey_no)
                    continue
            else:
                logger.info('Unsupported funckey type: %s', funckey_type)
                continue
            value = funckey_dict['value']
            label = escape(funckey_dict.get('label') or value)
            fkey_value = self._format_fkey_value(type_, value, suffix)
            lines.append('<fkey idx="%d" short_label="%s" label="%s" context="active" perm="R">%s</fkey>' %
                        (int(funckey_no) - 1, label, label, fkey_value))
        raw_config['XX_fkeys'] = '\n'.join(lines)

    def _format_fkey_value(self, fkey_type, value, suffix):
        return f'{fkey_type} {value}{suffix}'

    def _add_lang(self, raw_config):
        if 'locale' in raw_config:
            locale = raw_config['locale']
            if locale in self._LOCALE:
                raw_config['XX_lang'] = self._LOCALE[locale]

    def _format_dst_change(self, dst_change):
        fmted_time = '{:02d}:{:02d}:{:02d}'.format(*dst_change['time'].as_hms)
        day = dst_change['day']
        if day.startswith('D'):
            return f'{int(day[1:]):02d}.{dst_change["month"]:02d} {fmted_time}'

        week, weekday = list(map(int, day[1:].split('.')))
        weekday = tzinform.week_start_on_monday(weekday)
        return f'{dst_change["month"]:02d}.{week:02d}.{weekday:02d} {fmted_time}'

    def _format_tzinfo(self, tzinfo):
        lines = []
        lines.append('<timezone perm="R"></timezone>')
        lines.append(f'<utc_offset perm="R">{tzinfo["utcoffset"].as_seconds:+d}</utc_offset>')
        if tzinfo['dst'] is None:
            lines.append('<dst perm="R"></dst>')
        else:
            start = self._format_dst_change(tzinfo['dst']['start'])
            end = self._format_dst_change(tzinfo['dst']['end'])
            lines.append(f'<dst perm="R">{tzinfo["dst"]["save"].as_seconds:d} {start} {end}</dst>')
        return '\n'.join(lines)

    def _add_timezone(self, raw_config):
        if 'timezone' in raw_config:
            try:
                tzinfo = tzinform.get_timezone_info(raw_config['timezone'])
            except tzinform.TimezoneNotFoundError as e:
                logger.warning('Unknown timezone %s: %s', raw_config['timezone'], e)
            else:
                raw_config['XX_timezone'] = self._format_tzinfo(tzinfo)

    def _add_user_dtmf_info(self, raw_config):
        dtmf_mode = raw_config.get('sip_dtmf_mode')
        for line in raw_config['sip_lines'].values():
            cur_dtmf_mode = line.get('dtmf_mode', dtmf_mode)
            line['XX_user_dtmf_info'] = self._SIP_DTMF_MODE.get(cur_dtmf_mode, 'off')

    def _add_sip_transport(self, raw_config):
        raw_config['XX_sip_transport'] = self._SIP_TRANSPORT.get(raw_config.get('sip_transport'), 'udp')

    def _add_msgs_blocked(self, raw_config):
        msgs_blocked = ''
        for line_no, line in raw_config['sip_lines'].items():
            if line.get('backup_proxy_ip'):
                backup_line_no = int(line_no) + 1
                msgs_blocked += f' Identity{backup_line_no:02d}IsNotRegistered'
        raw_config['XX_msgs_blocked'] = msgs_blocked

    def _add_xivo_phonebook_url(self, raw_config):
        if hasattr(plugins, 'add_xivo_phonebook_url') and raw_config.get('config_version', 0) >= 1:
            plugins.add_xivo_phonebook_url(raw_config, 'snom')
        else:
            self._add_xivo_phonebook_url_compat(raw_config)

    def _add_xivo_phonebook_url_compat(self, raw_config):
        hostname = raw_config.get('X_xivo_phonebook_ip')
        if hostname:
            raw_config['XX_xivo_phonebook_url'] = 'http://{hostname}/service/ipbx/web_services.php/phonebook/search/'.format(hostname=hostname)

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
        fmted_mac = format_mac(device['mac'], separator='', uppercase=True)
        return f'snom{device["model"]}-{fmted_mac}.htm', fmted_mac + '.xml'

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

        model = device.get('model')
        self._update_sip_lines(raw_config)
        self._add_fkeys(raw_config, model)
        self._add_lang(raw_config)
        self._add_timezone(raw_config)
        self._add_user_dtmf_info(raw_config)
        self._add_sip_transport(raw_config)
        self._add_msgs_blocked(raw_config)
        self._add_xivo_phonebook_url(raw_config)
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

    if hasattr(synchronize, 'standard_sip_synchronize'):
        def synchronize(self, device, raw_config):
            return synchronize.standard_sip_synchronize(device, event='check-sync;reboot=false')

    else:
        # backward compatibility with older wazo-provd server
        def synchronize(self, device, raw_config):
            try:
                ip = device['ip'].encode('ascii')
            except KeyError:
                return defer.fail(Exception('IP address needed for device synchronization'))
            else:
                sync_service = synchronize.get_sync_service()
                if sync_service is None or sync_service.TYPE != 'AsteriskAMI':
                    return defer.fail(Exception(f'Incompatible sync service: {sync_service}'))
                else:
                    return threads.deferToThread(sync_service.sip_notify, ip, 'check-sync;reboot=false')

    def get_remote_state_trigger_filename(self, device):
        if 'mac' not in device or 'model' not in device:
            return None

        return self._dev_specific_filenames(device)[1]

    def is_sensitive_filename(self, filename):
        return bool(self._SENSITIVE_FILENAME_REGEX.match(filename))
