# -*- coding: UTF-8 -*-

__license__ = """
    Copyright (C) 2010-2011  Avencall

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import logging
import os.path
import re
from operator import itemgetter
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
    _PATH_REGEX = re.compile(r'\bsnom\w+-([\dA-F]{12})\.htm$')

    def extract(self, request, request_type):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request):
        ua = request.getHeader('User-Agent')
        if ua:
            dev_info = self._extract_from_ua(ua)
            if dev_info:
                self._extract_from_path(request.path, dev_info)
                return dev_info
        return None

    def _extract_from_ua(self, ua):
        # HTTP User-Agent:
        #   "Mozilla/4.0 (compatible; snom lid 3605)" --> Snom 6.5.xx
        #   "Mozilla/4.0 (compatible; snom320-SIP 6.5.20; snom320 jffs2 v3.36; snom320 linux 3.38)"
        #   "Mozilla/4.0 (compatible; snom320-SIP 7.3.30 1.1.3-u)"
        #   "Mozilla/4.0 (compatible; snom320-SIP 8.4.18 1.1.3-s)"
        #   "Mozilla/4.0 (compatible; snom820-SIP 8.4.18 1.1.4-IFX-26.11.09)"
        #   "Mozilla/4.0 (compatible; snom870-SIP 8.3.6 SPEAr300 SNOM 1.4)"
        #   "Mozilla/4.0 (compatible; snom870-SIP 8.4.18 SPEAr300 SNOM 1.4)"
        #   "Mozilla/4.0 (compatible; snom820-SIP 8.4.35 1.1.4-IFX-26.11.09)"
        #   "Mozilla/4.0 (compatible; snom870-SIP 8.4.35 SPEAr300 SNOM 1.4)"
        #   "Mozilla/4.0 (compatible; snomPA1-SIP 8.4.23 1.1.3-s)"
        #   "Mozilla/4.0 (compatible; snomPA1-SIP 8.4.35 1.1.3-s)"
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
            maj_version = int(version[0])
            if maj_version < 7:
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

    def _get_fkey_domain(self, raw_config):
        # Return None if there's no usable domain
        if u'sip_proxy_ip' in raw_config:
            return raw_config[u'sip_proxy_ip']
        else:
            lines = raw_config[u'sip_lines']
            if lines:
                return lines[min(lines.iterkeys())][u'proxy_ip']
        return None

    def _add_fkeys(self, raw_config):
        domain = self._get_fkey_domain(raw_config)
        if domain is None:
            if raw_config[u'funckeys']:
                logger.warning('Could not set funckeys: no domain part')
        else:
            lines = []
            for funckey_no, funckey_dict in sorted(raw_config[u'funckeys'].iteritems(),
                                                   key=itemgetter(0)):
                funckey_type = funckey_dict[u'type']
                if funckey_type == u'speeddial':
                    type_ = u'speed'
                    suffix = ''
                elif funckey_type == u'blf':
                    if u'exten_pickup_call' in raw_config:
                        type_ = u'blf'
                        suffix = '|%s' % raw_config[u'exten_pickup_call']
                    else:
                        logger.warning('Could not set funckey %s: no exten_pickup_call',
                                       funckey_no)
                        continue
                else:
                    logger.info('Unsupported funckey type: %s', funckey_type)
                    continue
                value = funckey_dict[u'value']
                lines.append(u'<fkey idx="%d" context="active" perm="R">%s &lt;sip:%s@%s&gt;%s</fkey>' %
                            (int(funckey_no) - 1, type_, value, domain, suffix))
            raw_config[u'XX_fkeys'] = u'\n'.join(lines)

    def _add_lang(self, raw_config):
        if u'locale' in raw_config:
            locale = raw_config[u'locale']
            if locale in self._LOCALE:
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
        if u'timezone' in raw_config:
            try:
                tzinfo = tzinform.get_timezone_info(raw_config[u'timezone'])
            except tzinform.TimezoneNotFoundError, e:
                logger.warning('Unknown timezone %s: %s', raw_config[u'timezone'], e)
            else:
                raw_config[u'XX_timezone'] = self._format_tzinfo(tzinfo)

    def _add_user_dtmf_info(self, raw_config):
        dtmf_mode = raw_config.get(u'sip_dtmf_mode')
        for line in raw_config[u'sip_lines'].itervalues():
            cur_dtmf_mode = line.get(u'dtmf_mode', dtmf_mode)
            line[u'XX_user_dtmf_info'] = self._SIP_DTMF_MODE.get(cur_dtmf_mode, u'off')

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

        self._add_fkeys(raw_config)
        self._add_lang(raw_config)
        self._add_timezone(raw_config)
        self._add_user_dtmf_info(raw_config)

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
