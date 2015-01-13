# -*- coding: utf-8 -*-

# Copyright (C) 2011-2015 Avencall
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

import logging
import re
import os.path
from operator import itemgetter
from provd import tzinform
from provd import synchronize
from provd.devices.config import RawConfigError
from provd.devices.pgasso import IMPROBABLE_SUPPORT, PROBABLE_SUPPORT,\
    COMPLETE_SUPPORT, FULL_SUPPORT, BasePgAssociator
from provd.plugins import StandardPlugin, FetchfwPluginHelper,\
    TemplatePluginHelper
from provd.servers.http import HTTPNoListingFileService
from provd.util import norm_mac, format_mac
from twisted.internet import defer, threads

logger = logging.getLogger('plugin.xivo-yealink')


class BaseYealinkHTTPDeviceInfoExtractor(object):
    _UA_REGEX_LIST = [
        re.compile(r'^[yY]ealink\s+SIP-(\w+)\s+([\d.]+)\s+([\da-f:]{17})$'),
        re.compile(r'(VP530P?|W52P)\s+([\d.]+)\s+([\da-f:]{17})$'),
        re.compile(r'[yY]ealink-(\w+)\s+([\d.]+)\s+([\d.]+)$'),
    ]

    def extract(self, request, request_type):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request):
        ua = request.getHeader('User-Agent')
        if ua:
            return self._extract_from_ua(ua)
        else:
            return self._extract_from_path(request)

    def _extract_from_ua(self, ua):
        # HTTP User-Agent:
        #   "yealink SIP-T18 18.0.0.80 00:15:65:27:3e:05"
        #   "Yealink SIP-T20P 9.72.0.30 00:15:65:5e:16:7c"
        #   "Yealink SIP-T21P 34.72.0.1 00:15:65:4c:4c:26"
        #   "Yealink SIP-T22P 7.72.0.30 00:15:65:39:31:fc"
        #   "Yealink SIP-T26P 6.72.0.30 00:15:65:4b:57:d2"
        #   "yealink SIP-T28P 2.70.0.140 00:15:65:13:ae:0b"
        #   "Yealink SIP-T38G  38.70.0.125 00:15:65:2f:c3:5e"
        #   "Yealink SIP-T41P 36.72.0.1 00:15:65:53:83:22"
        #   "Yealink SIP-T42G 29.72.0.1 00:15:65:4c:3b:b0"
        #   "Yealink SIP-T46G 28.72.0.1 00:15:65:4a:a9:37"
        #   "Yealink SIP-T48G 35.72.0.6 00:15:65:5c:60:82"
        #   "Yealink SIP-W52P 25.73.0.20 00:15:65:40:ae:35"
        #   "W52P 25.30.0.2 00:15:65:44:b3:7c"
        #   "Yealink-T46G 28.71.0.81 28.1.0.128.0.0.0"
        #   "VP530P 23.70.0.40 00:15:65:31:4b:c0"
        #   "VP530 23.70.0.41 00:15:65:3d:58:e3"

        for UA_REGEX in self._UA_REGEX_LIST:
            m = UA_REGEX.match(ua)
            if m:
                raw_model, raw_version, raw_mac = m.groups()
                try:
                    mac = norm_mac(raw_mac.decode('ascii'))
                except ValueError as e:
                    logger.warning('Could not normalize MAC address "%s": %s', raw_mac, e)
                    return {u'vendor': u'Yealink',
                            u'model': raw_model.decode('ascii'),
                            u'version': raw_version.decode('ascii')}
                else:
                    return {u'vendor': u'Yealink',
                            u'model': raw_model.decode('ascii'),
                            u'version': raw_version.decode('ascii'),
                            u'mac': mac}
        return None

    def _extract_from_path(self, request):
        if request.path.startswith('/001565'):
            raw_mac = path[1:-4]
            try:
                mac = norm_mac(raw_mac.decode('ascii'))
            except ValueError as e:
                logger.warning('Could not normalize MAC address "%s": %s', raw_mac, e)
            else:
                return {u'mac': mac}
        if request.path.startswith('/y000000000025.cfg'):
            return {u'vendor': u'Yealink',
                    u'model' : u'W52P'}
        return None


class BaseYealinkPgAssociator(BasePgAssociator):
    def __init__(self, model_versions):
        # model_versions is a dictionary which keys are model IDs and values
        # are version IDs.
        BasePgAssociator.__init__(self)
        self._model_versions = model_versions

    def _do_associate(self, vendor, model, version):
        if vendor == u'Yealink':
            if model in self._model_versions:
                if version == self._model_versions[model]:
                    return FULL_SUPPORT
                return COMPLETE_SUPPORT
            return PROBABLE_SUPPORT
        return IMPROBABLE_SUPPORT


class BaseYealinkPlugin(StandardPlugin):
    _ENCODING = 'UTF-8'
    _LOCALE = {
        u'de_DE': (u'German', u'Germany', u'2'),
        u'en_US': (u'English', u'United States', u'0'),
        u'es_ES': (u'Spanish', u'Spain', u'6'),
        u'fr_FR': (u'French', u'France', u'1'),
        u'fr_CA': (u'French', u'United States', u'1'),
    }
    _SIP_DTMF_MODE = {
        u'RTP-in-band': u'0',
        u'RTP-out-of-band': u'1',
        u'SIP-INFO': u'2',
    }

    def __init__(self, app, plugin_dir, gen_cfg, spec_cfg):
        StandardPlugin.__init__(self, app, plugin_dir, gen_cfg, spec_cfg)

        self._tpl_helper = TemplatePluginHelper(plugin_dir)

        downloaders = FetchfwPluginHelper.new_downloaders(gen_cfg.get('proxies'))
        fetchfw_helper = FetchfwPluginHelper(plugin_dir, downloaders)

        self.services = fetchfw_helper.services()
        self.http_service = HTTPNoListingFileService(self._tftpboot_dir)

    http_dev_info_extractor = BaseYealinkHTTPDeviceInfoExtractor()

    def configure_common(self, raw_config):
        for filename, fw_filename, tpl_filename in self._COMMON_FILES:
            tpl = self._tpl_helper.get_template('common/%s' % tpl_filename)
            dst = os.path.join(self._tftpboot_dir, filename)
            raw_config[u'XX_fw_filename'] = fw_filename
            self._tpl_helper.dump(tpl, raw_config, dst, self._ENCODING)

    def _update_sip_lines(self, raw_config):
        for line_no, line in raw_config['sip_lines'].iteritems():
            # set line number
            line[u'XX_line_no'] = int(line_no)
            # set dtmf inband transfer
            dtmf_mode = line.get(u'dtmf_mode') or raw_config.get(u'sip_dtmf_mode')
            if dtmf_mode in self._SIP_DTMF_MODE:
                line[u'XX_dtmf_type'] = self._SIP_DTMF_MODE[dtmf_mode]
            # set voicemail
            if u'voicemail' not in line and u'exten_voicemail' in raw_config:
                line[u'voicemail'] = raw_config[u'exten_voicemail']
            # set proxy_ip
            if u'proxy_ip' not in line:
                line[u'proxy_ip'] = raw_config[u'sip_proxy_ip']
            # set proxy_port
            if u'proxy_port' not in line and u'sip_proxy_port' in raw_config:
                line[u'proxy_port'] = raw_config[u'sip_proxy_port']

    def _format_funckey_speeddial(self, funckey_no, funckey_dict):
        lines = []
        lines.append(u'memorykey.%s.line = %s' % (funckey_no, funckey_dict.get(u'line', 1)))
        lines.append(u'memorykey.%s.value = %s' % (funckey_no, funckey_dict[u'value']))
        lines.append(u'memorykey.%s.type = 13' % funckey_no)
        lines.append(u'memorykey.%s.label = %s' % (funckey_no, funckey_dict.get(u'label', u'')))
        return lines

    def _format_funckey_call_park(self, funckey_no, funckey_dict):
        lines = []
        lines.append(u'memorykey.%s.line = %s' % (funckey_no, funckey_dict.get(u'line', 1)))
        lines.append(u'memorykey.%s.value = %s' % (funckey_no, funckey_dict[u'value']))
        lines.append(u'memorykey.%s.type = 10' % funckey_no)
        lines.append(u'memorykey.%s.label = %s' % (funckey_no, funckey_dict.get(u'label', u'')))
        return lines

    def _format_funckey_blf(self, funckey_no, funckey_dict, exten_pickup_call=None):
        # Be warned that blf works only for DSS keys.
        lines = []
        lines.append(u'memorykey.%s.line = %s' % (funckey_no, funckey_dict.get(u'line', 1) - 1))
        value = funckey_dict[u'value']
        lines.append(u'memorykey.%s.value = %s' % (funckey_no, value))
        lines.append(u'memorykey.%s.label = %s' % (funckey_no, funckey_dict.get(u'label', u'')))
        lines.append(u'memorykey.%s.sub_type = blf' % funckey_no)
        if exten_pickup_call:
            lines.append(u'memorykey.%s.pickup_value = %s' % (funckey_no, exten_pickup_call))
        lines.append(u'memorykey.%s.type = 16' % funckey_no)
        return lines

    def _add_fkeys(self, raw_config, device):
        # XXX maybe rework this, a bit ugly
        lines = []
        exten_pickup_call = raw_config.get('exten_pickup_call')
        for funckey_no, funckey_dict in sorted(raw_config[u'funckeys'].iteritems(),
                                               key=itemgetter(0)):
            keynum = int(funckey_no)
            funckey_type = funckey_dict[u'type']
            if funckey_type == u'speeddial':
                lines.extend(self._format_funckey_speeddial(funckey_no, funckey_dict))
            elif funckey_type == u'blf':
                if keynum <= 10:
                    lines.extend(self._format_funckey_blf(funckey_no, funckey_dict,
                                                          exten_pickup_call))
                else:
                    logger.info('For Yealink, blf is only available on DSS keys')
                    lines.extend(self._format_funckey_speeddial(funckey_no, funckey_dict))
            elif funckey_type == u'park':
                lines.extend(self._format_funckey_call_park(funckey_no, funckey_dict))
            else:
                logger.info('Unsupported funckey type: %s', funckey_type)
                continue
            lines.append(u'')
        raw_config[u'XX_fkeys'] = u'\n'.join(lines)

    def _add_country_and_lang(self, raw_config):
        locale = raw_config.get(u'locale')
        if locale in self._LOCALE:
            (raw_config[u'XX_lang'],
             raw_config[u'XX_country'],
             raw_config[u'XX_handset_lang']) = self._LOCALE[locale]

    def _format_dst_change(self, dst_change):
        if dst_change['day'].startswith('D'):
            return u'%02d/%02d/%02d' % (dst_change['month'], dst_change['day'][1:], dst_change['time'].as_hour)
        else:
            week, weekday = map(int, dst_change['day'][1:].split('.'))
            weekday = tzinform.week_start_on_monday(weekday)
            return u'%d/%d/%d/%d' % (dst_change['month'], week, weekday, dst_change['time'].as_hours)

    def _format_tz_info(self, tzinfo):
        lines = []
        lines.append(u'local_time.time_zone = %+d' % min(max(tzinfo['utcoffset'].as_hours, -11), 12))
        if tzinfo['dst'] is None:
            lines.append(u'local_time.summer_time = 0')
        else:
            lines.append(u'local_time.summer_time = 1')
            if tzinfo['dst']['start']['day'].startswith('D'):
                lines.append(u'local_time.dst_time_type = 0')
            else:
                lines.append(u'local_time.dst_time_type = 1')
            lines.append(u'local_time.start_time = %s' % self._format_dst_change(tzinfo['dst']['start']))
            lines.append(u'local_time.end_time = %s' % self._format_dst_change(tzinfo['dst']['end']))
            lines.append(u'local_time.offset_time = %s' % tzinfo['dst']['save'].as_minutes)
        return u'\n'.join(lines)

    def _add_timezone(self, raw_config):
        if u'timezone' in raw_config:
            try:
                tzinfo = tzinform.get_timezone_info(raw_config[u'timezone'])
            except tzinform.TimezoneNotFoundError, e:
                logger.warning('Unknown timezone: %s', e)
            else:
                raw_config[u'XX_timezone'] = self._format_tz_info(tzinfo)

    def _dev_specific_filename(self, device):
        # Return the device specific filename (not pathname) of device
        fmted_mac = format_mac(device[u'mac'], separator='')
        return fmted_mac + '.cfg'

    def _check_config(self, raw_config):
        if u'http_port' not in raw_config:
            raise RawConfigError('only support configuration via HTTP')

    def _check_device(self, device):
        if u'mac' not in device:
            raise Exception('MAC address needed for device configuration')

    def configure(self, device, raw_config):
        self._check_config(raw_config)
        self._check_device(device)
        filename = self._dev_specific_filename(device)
        tpl = self._tpl_helper.get_dev_template(filename, device)

        self._add_fkeys(raw_config, device)
        self._add_country_and_lang(raw_config)
        self._add_timezone(raw_config)
        self._update_sip_lines(raw_config)
        raw_config[u'XX_options'] = device.get(u'options', {})

        path = os.path.join(self._tftpboot_dir, filename)
        self._tpl_helper.dump(tpl, raw_config, path, self._ENCODING)

    def deconfigure(self, device):
        path = os.path.join(self._tftpboot_dir, self._dev_specific_filename(device))
        try:
            os.remove(path)
        except OSError, e:
            # ignore
            logger.info('error while removing file: %s', e)

    if hasattr(synchronize, 'standard_sip_synchronize'):
        def synchronize(self, device, raw_config):
            return synchronize.standard_sip_synchronize(device)

    else:
        # backward compatibility with older xivo-provd server
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
                    return threads.deferToThread(sync_service.sip_notify, ip, 'check-sync')

    def get_remote_state_trigger_filename(self, device):
        if u'mac' not in device:
            return None

        return self._dev_specific_filename(device)
