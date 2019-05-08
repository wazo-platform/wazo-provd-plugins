# -*- coding: utf-8 -*-

# Copyright 2010-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import os.path
import re
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


class BaseSnomHTTPDeviceInfoExtractor(object):
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
            device_info[u'mac'] = norm_mac(raw_mac.decode('ascii'))
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
            return {u'vendor': u'Snom',
                    u'model': raw_model.decode('ascii'),
                    u'mac': norm_mac(raw_mac.decode('ascii')),
                    u'version': raw_version.decode('ascii')}
        # if the complete regex did not match, match a smaller one
        m = self._UA_REGEX.search(ua)
        if m:
            raw_model, raw_version = m.groups()
            return {u'vendor': u'Snom',
                    u'model': raw_model.decode('ascii'),
                    u'version': raw_version.decode('ascii')}
        return None

    def _extract_from_path(self, path, dev_info):
        m = self._PATH_REGEX.search(path)
        if m:
            raw_mac = m.group(1)
            dev_info[u'mac'] = norm_mac(raw_mac.decode('ascii'))


class BaseSnomPgAssociator(BasePgAssociator):
    def __init__(self, models, version):
        self._models = models
        self._version = version

    def _do_associate(self, vendor, model, version):
        if vendor == u'Snom':
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
        u'de_DE': (u'Deutsch', u'GER'),
        u'en_US': (u'English', u'USA'),
        u'es_ES': (u'Espanol', u'ESP'),
        u'fr_FR': (u'Francais', u'FRA'),
        u'fr_CA': (u'Francais', u'USA'),
        u'it_IT': (u'Italiano', u'ITA'),
        u'nl_NL': (u'Dutch', u'NLD'),
    }
    _SIP_DTMF_MODE = {
        u'RTP-in-band': u'off',
        u'RTP-out-of-band': u'off',
        u'SIP-INFO': u'sip_info_only'
    }
    _XX_DICT_DEF = u'en'
    _XX_DICT = {
        u'en': {
            u'remote_directory': u'Directory',
        },
        u'fr': {
            u'remote_directory': u'Annuaire',
        },
    }

    _SENSITIVE_FILENAME_REGEX = re.compile(r'^[0-9A-F]{12}\.xml')

    def __init__(self, app, plugin_dir, gen_cfg, spec_cfg):
        StandardPlugin.__init__(self, app, plugin_dir, gen_cfg, spec_cfg)

        self._tpl_helper = TemplatePluginHelper(plugin_dir)

        downloaders = FetchfwPluginHelper.new_downloaders(gen_cfg.get('proxies'))
        fetchfw_helper = FetchfwPluginHelper(plugin_dir, downloaders)

        self.services = fetchfw_helper.services()
        self.http_service = HTTPNoListingFileService(self._tftpboot_dir)

    http_dev_info_extractor = BaseSnomHTTPDeviceInfoExtractor()

    def _common_templates(self):
        yield ('common/gui_lang.xml.tpl', 'gui_lang.xml')
        yield ('common/web_lang.xml.tpl', 'web_lang.xml')
        for tpl_format, file_format in [('common/snom%s.htm.tpl', 'snom%s.htm'),
                                        ('common/snom%s.xml.tpl', 'snom%s.xml'),
                                        ('common/snom%s-firmware.xml.tpl', 'snom%s-firmware.xml')]:
            for model in self._MODELS:
                yield tpl_format % model, file_format % model

    def configure_common(self, raw_config):
        for tpl_filename, filename in self._common_templates():
            tpl = self._tpl_helper.get_template(tpl_filename)
            dst = os.path.join(self._tftpboot_dir, filename)
            self._tpl_helper.dump(tpl, raw_config, dst, self._ENCODING)

    def _update_sip_lines(self, raw_config):
        proxy_ip = raw_config.get(u'sip_proxy_ip')
        backup_proxy_ip = raw_config.get(u'sip_backup_proxy_ip')
        voicemail = raw_config.get(u'exten_voicemail')
        for line in raw_config[u'sip_lines'].itervalues():
            if proxy_ip:
                line.setdefault(u'proxy_ip', proxy_ip)
            if backup_proxy_ip:
                line.setdefault(u'backup_proxy_ip', backup_proxy_ip)
            if voicemail:
                line.setdefault(u'voicemail', voicemail)

    def _add_fkeys(self, raw_config, model):
        lines = []
        for funckey_no, funckey_dict in sorted(raw_config[u'funckeys'].iteritems(),
                                               key=itemgetter(0)):
            funckey_type = funckey_dict[u'type']
            if funckey_type == u'speeddial':
                type_ = u'speed'
                suffix = ''
            elif funckey_type == u'park':
                if model in [u'710', u'715', u'720', u'725', u'760', u'D765']:
                    type_ = u'orbit'
                    suffix = ''
                else:
                    type_ = u'speed'
                    suffix = ''
            elif funckey_type == u'blf':
                exten_pickup_call = raw_config.get(u'exten_pickup_call')
                if exten_pickup_call:
                    type_ = u'blf'
                    suffix = '|%s' % exten_pickup_call
                else:
                    logger.warning('Could not set funckey %s: no exten_pickup_call',
                                   funckey_no)
                    continue
            else:
                logger.info('Unsupported funckey type: %s', funckey_type)
                continue
            value = funckey_dict[u'value']
            label = escape(funckey_dict.get(u'label') or value)
            fkey_value = self._format_fkey_value(type_, value, suffix)
            lines.append(u'<fkey idx="%d" label="%s" context="active" perm="R">%s</fkey>' %
                         (int(funckey_no) - 1, label, fkey_value))
        raw_config[u'XX_fkeys'] = u'\n'.join(lines)

    def _format_fkey_value(self, fkey_type, value, suffix):
        return '%s %s%s' % (fkey_type, value, suffix)

    def _add_lang(self, raw_config):
        locale = raw_config.get(u'locale')
        if locale and locale in self._LOCALE:
            raw_config[u'XX_lang'] = self._LOCALE[locale]

    def _format_dst_change(self, dst_change):
        fmted_time = u'%02d:%02d:%02d' % tuple(dst_change['time'].as_hms)
        day = dst_change['day']
        if day.startswith('D'):
            return u'%02d.%02d %s' % (int(day[1:]), dst_change['month'], fmted_time)
        else:
            week, weekday = map(int, day[1:].split('.'))
            weekday = tzinform.week_start_on_monday(weekday)
            return u'%02d.%02d.%02d %s' % (dst_change['month'], week, weekday, fmted_time)

    def _format_tzinfo(self, tzinfo):
        lines = []
        lines.append(u'<timezone perm="R"></timezone>')
        lines.append(u'<utc_offset perm="R">%+d</utc_offset>' % tzinfo['utcoffset'].as_seconds)
        if tzinfo['dst'] is None:
            lines.append(u'<dst perm="R"></dst>')
        else:
            lines.append(u'<dst perm="R">%d %s %s</dst>' %
                         (tzinfo['dst']['save'].as_seconds,
                          self._format_dst_change(tzinfo['dst']['start']),
                          self._format_dst_change(tzinfo['dst']['end'])))
        return u'\n'.join(lines)

    def _add_timezone(self, raw_config):
        timezone = raw_config.get(u'timezone')
        if timezone:
            try:
                tzinfo = tzinform.get_timezone_info(timezone)
            except tzinform.TimezoneNotFoundError, e:
                logger.warning('Unknown timezone %s: %s', timezone, e)
            else:
                raw_config[u'XX_timezone'] = self._format_tzinfo(tzinfo)

    def _add_user_dtmf_info(self, raw_config):
        dtmf_mode = raw_config.get(u'sip_dtmf_mode')
        for line in raw_config[u'sip_lines'].itervalues():
            cur_dtmf_mode = line.get(u'dtmf_mode', dtmf_mode)
            line[u'XX_user_dtmf_info'] = self._SIP_DTMF_MODE.get(cur_dtmf_mode, u'off')

    def _add_msgs_blocked(self, raw_config):
        msgs_blocked = ''
        for line_no, line in raw_config[u'sip_lines'].iteritems():
            if line.get('backup_proxy_ip'):
                backup_line_no = int(line_no) + 1
                msgs_blocked += ' Identity%02dIsNotRegistered' % backup_line_no
        raw_config['XX_msgs_blocked'] = msgs_blocked

    def _add_xivo_phonebook_url(self, raw_config):
        if hasattr(plugins, 'add_xivo_phonebook_url') and raw_config.get(u'config_version', 0) >= 1:
            plugins.add_xivo_phonebook_url(raw_config, u'snom')
        else:
            self._add_xivo_phonebook_url_compat(raw_config)

    def _add_xivo_phonebook_url_compat(self, raw_config):
        hostname = raw_config.get(u'X_xivo_phonebook_ip')
        if hostname:
            raw_config[u'XX_xivo_phonebook_url'] = u'http://{hostname}/service/ipbx/web_services.php/phonebook/search/'.format(hostname=hostname)

    def _gen_xx_dict(self, raw_config):
        xx_dict = self._XX_DICT[self._XX_DICT_DEF]
        locale = raw_config.get(u'locale')
        if locale:
            lang = locale.split('_', 1)[0]
            if lang in self._XX_DICT:
                xx_dict = self._XX_DICT[lang]
        return xx_dict

    def _dev_specific_filenames(self, device):
        # Return a tuple (htm filename, xml filename)
        fmted_mac = format_mac(device[u'mac'], separator='', uppercase=True)
        return 'snom%s-%s.htm' % (device[u'model'], fmted_mac), fmted_mac + '.xml'

    def _check_config(self, raw_config):
        if u'http_port' not in raw_config:
            raise RawConfigError('only support configuration via HTTP')

    def _check_device(self, device):
        if u'mac' not in device:
            raise Exception('MAC address needed for device configuration')
        # model is needed since filename has model name in it.
        if u'model' not in device:
            raise Exception('model needed for device configuration')

    def configure(self, device, raw_config):
        self._check_config(raw_config)
        self._check_device(device)
        htm_filename, xml_filename = self._dev_specific_filenames(device)

        # generate xml file
        tpl = self._tpl_helper.get_dev_template(xml_filename, device)

        model = device.get(u'model')
        self._update_sip_lines(raw_config)
        self._add_fkeys(raw_config, model)
        self._add_lang(raw_config)
        self._add_timezone(raw_config)
        self._add_user_dtmf_info(raw_config)
        self._add_msgs_blocked(raw_config)
        self._add_xivo_phonebook_url(raw_config)
        raw_config[u'XX_dict'] = self._gen_xx_dict(raw_config)
        raw_config[u'XX_options'] = device.get(u'options', {})

        path = os.path.join(self._tftpboot_dir, xml_filename)
        self._tpl_helper.dump(tpl, raw_config, path, self._ENCODING)

        # generate htm file
        tpl = self._tpl_helper.get_template('other/base.htm.tpl')

        raw_config[u'XX_xml_filename'] = xml_filename

        path = os.path.join(self._tftpboot_dir, htm_filename)
        self._tpl_helper.dump(tpl, raw_config, path, self._ENCODING)

    def deconfigure(self, device):
        for filename in self._dev_specific_filenames(device):
            try:
                os.remove(os.path.join(self._tftpboot_dir, filename))
            except OSError, e:
                # ignore
                logger.info('error while removing file: %s', e)

    if hasattr(synchronize, 'standard_sip_synchronize'):
        def synchronize(self, device, raw_config):
            return synchronize.standard_sip_synchronize(device, event='check-sync;reboot=true')

    else:
        # backward compatibility with older wazo-provd server
        def synchronize(self, device, raw_config):
            try:
                ip = device[u'ip'].encode('ascii')
            except KeyError:
                return defer.fail(Exception('IP address needed for device synchronization'))
            else:
                sync_service = synchronize.get_sync_service()
                if sync_service is None or sync_service.TYPE != 'AsteriskAMI':
                    return defer.fail(Exception('Incompatible sync service: %s' % sync_service))
                else:
                    return threads.deferToThread(sync_service.sip_notify, ip, 'check-sync;reboot=true')

    def get_remote_state_trigger_filename(self, device):
        if u'mac' not in device or u'model' not in device:
            return None

        return self._dev_specific_filenames(device)[1]

    def is_sensitive_filename(self, filename):
        return bool(self._SENSITIVE_FILENAME_REGEX.match(filename))
