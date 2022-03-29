# -*- coding: utf-8 -*-

# Copyright 2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import os.path
import re
from provd import plugins
from provd import tzinform
from provd import synchronize
from provd.devices.config import RawConfigError
from provd.devices.pgasso import (
    BasePgAssociator,
    COMPLETE_SUPPORT,
    FULL_SUPPORT,
    IMPROBABLE_SUPPORT,
    PROBABLE_SUPPORT,
)
from provd.plugins import (
    FetchfwPluginHelper,
    StandardPlugin,
    TemplatePluginHelper,
)
from provd.servers.http import HTTPNoListingFileService
from provd.util import format_mac, norm_mac
from twisted.internet import defer, threads

logger = logging.getLogger('plugin.wazo-alcatel')


class BaseAlcatelMyriadHTTPDeviceInfoExtractor(object):
    _UA_REGEX_MAC = re.compile(
        r'^ALE (?P<model>M[3,5,7])(?:-CE)? (?P<version>([0-9]{1,4}\.?){4,5}) (?P<mac>[0-9a-f]{12})'
    )

    def extract(self, request, request_type):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request):
        device_info = {}
        ua = request.getHeader('User-Agent')
        raw_mac = request.args.get('mac', [None])[0]
        if raw_mac:
            logger.debug('Got MAC from URL: "%s"', raw_mac)
            device_info[u'mac'] = norm_mac(raw_mac.decode('ascii'))
        if ua:
            info_from_ua = self._extract_from_ua(ua)
            if info_from_ua:
                device_info.update(info_from_ua)
        return device_info

    def _extract_from_ua(self, ua):
        # HTTP User-Agent:
        #   "ALE M3-CE 2.11.01.1604 3c28a620089e"
        m = self._UA_REGEX_MAC.search(ua)
        if m:
            device_info = m.groupdict()
            raw_model = device_info['model']
            raw_version = device_info['version']
            raw_mac = device_info['mac']
            return {
                u'vendor': u'Alcatel-Lucent',
                u'model': raw_model.decode('ascii'),
                u'mac': norm_mac(raw_mac.decode('ascii')),
                u'version': raw_version.decode('ascii'),
            }


class BaseAlcatelMyriadPgAssociator(BasePgAssociator):
    def __init__(self, models_versions):
        self._models_versions = models_versions

    def _do_associate(self, vendor, model, version):
        if vendor == u'Alcatel-Lucent':
            if model in self._models_versions:
                if version == self._models_versions.get(model, None):
                    return FULL_SUPPORT
                return COMPLETE_SUPPORT
            return PROBABLE_SUPPORT
        return IMPROBABLE_SUPPORT


class BaseAlcatelPlugin(StandardPlugin):
    _ENCODING = 'UTF-8'

    _SIP_DTMF_MODE = {
        u'off': 0,
        u'RTP-in-band': 1,
        u'RTP-out-of-band': 2,
        u'SIP-INFO': 4,
    }

    _NB_FUNCKEYS = {
        u'M3': 20,
        u'M5': 28,
        u'M7': 28,
    }
    _FUNCKEY_TYPE = {
        u'blf': 59,
        u'speeddial': 1,
    }
    _LANG = {
        u'en': 0,
        u'fr': 1,
        u'de': 2,
        u'it': 3,
        u'es': 4,
        u'nl': 5,
        u'pt': 6,
        u'hu': 7,
        u'cs': 8,
        u'sk': 9,
        u'sl': 10,
        u'et': 11,
        u'pl': 12,
        u'lt': 13,
        u'lv': 14,
        u'tr': 15,
        u'el': 16,
        u'sv': 17,
        u'no': 18,
        u'da': 19,
        u'fi': 20,
        u'is': 21,
        u'zh': 22,
    }

    _SENSITIVE_FILENAME_REGEX = re.compile(r'^config\.[0-9a-f]{12}\.xml')
    http_dev_info_extractor = BaseAlcatelMyriadHTTPDeviceInfoExtractor()

    def __init__(self, app, plugin_dir, gen_cfg, spec_cfg):
        StandardPlugin.__init__(self, app, plugin_dir, gen_cfg, spec_cfg)

        self._tpl_helper = TemplatePluginHelper(plugin_dir)

        downloaders = FetchfwPluginHelper.new_downloaders(gen_cfg.get('proxies'))
        fetchfw_helper = FetchfwPluginHelper(plugin_dir, downloaders)

        self.services = fetchfw_helper.services()
        self.http_service = HTTPNoListingFileService(self._tftpboot_dir)

    def _common_templates(self):
        for tpl_format, file_format in [('common/config.model.xml.tpl', 'config.{}.xml')]:
            for model in self._MODELS_VERSIONS:
                yield tpl_format.format(model), file_format.format(model)

    def configure_common(self, raw_config):
        self._add_server_url(raw_config)
        for tpl_filename, filename in self._common_templates():
            tpl = self._tpl_helper.get_template(tpl_filename)
            dest_file = os.path.join(self._tftpboot_dir, filename)
            self._tpl_helper.dump(tpl, raw_config, dest_file, self._ENCODING)

    def _update_sip_lines(self, raw_config):
        proxy_ip = raw_config.get(u'sip_proxy_ip')
        proxy_port = raw_config.get(u'sip_proxy_port')
        backup_proxy_ip = raw_config.get(u'sip_backup_proxy_ip')
        backup_proxy_port = raw_config.get(u'sip_backup_proxy_port')
        outbound_proxy_ip = raw_config.get(u'sip_outbound_proxy_ip')
        outbound_proxy_port = raw_config.get(u'sip_outbound_proxy_port')
        voicemail = raw_config.get(u'exten_voicemail')

        for line in raw_config[u'sip_lines'].itervalues():
            if proxy_ip:
                line.setdefault(u'proxy_ip', proxy_ip)
            if proxy_port:
                line.setdefault(u'proxy_port', proxy_port)
            if backup_proxy_ip:
                line.setdefault(u'backup_proxy_ip', backup_proxy_ip)
            if backup_proxy_port:
                line.setdefault(u'backup_proxy_port', backup_proxy_port)
            if outbound_proxy_ip:
                line.setdefault(u'outbound_proxy_ip', outbound_proxy_ip)
            if outbound_proxy_port:
                line.setdefault(u'outbound_proxy_port', outbound_proxy_port)
            if voicemail:
                line.setdefault(u'voicemail', voicemail)

    def _add_fkeys(self, raw_config, model):
        nb_funckeys = self._NB_FUNCKEYS.get(model)
        if not nb_funckeys:
            logger.warning('Unknown model: "%s". Skipping function key configuration.', model)
            return

        raw_config[u'XX_fkeys'] = []
        for funckey_no, funckey_dict in raw_config[u'funckeys'].iteritems():
            position = int(funckey_no) + 1
            fkey_type = self._FUNCKEY_TYPE.get(
                funckey_dict[u'type'], self._FUNCKEY_TYPE[u'speeddial']
            )
            fkey_label = funckey_dict[u'label']
            fkey_extension = funckey_dict[u'value']
            if position > nb_funckeys:
                logger.warning('Function key "%s" outside range supported by phone.', position)
                continue
            fkey_data = {
                u'position': position,
                u'type': fkey_type,
                u'label': fkey_label,
                u'extension': fkey_extension,
                u'value': fkey_extension,
            }
            raw_config[u'XX_fkeys'].append(fkey_data)

    def _format_tzinfo(self, tzinfo):
        tz_hms = tzinfo['utcoffset'].as_hms
        offset_hour = tz_hms[0]
        offset_minutes = tz_hms[1]
        return '{:+02d}:{:02d}'.format(offset_hour, offset_minutes)

    def _add_timezone(self, raw_config):
        if u'timezone' in raw_config:
            try:
                tzinfo = tzinform.get_timezone_info(raw_config[u'timezone'])
            except tzinform.TimezoneNotFoundError as e:
                logger.warning('Unknown timezone "%s": "%s"', raw_config[u'timezone'], e)
            else:
                raw_config[u'XX_timezone'] = self._format_tzinfo(tzinfo)

    def _add_language(self, raw_config):
        locale = raw_config[u'locale']
        if '_' in locale:
            lang, _ = locale.split('_')
        else:
            lang = locale

        lang_code = self._LANG.get(lang, self._LANG['en'])
        raw_config[u'XX_lang'] = lang_code

    def _add_user_dtmf_info(self, raw_config):
        dtmf_mode = raw_config.get(u'sip_dtmf_mode')
        for line in raw_config[u'sip_lines'].itervalues():
            cur_dtmf_mode = line.get(u'dtmf_mode', dtmf_mode)
            line[u'XX_user_dtmf_info'] = self._SIP_DTMF_MODE.get(cur_dtmf_mode, 'off')

    def _add_xivo_phonebook_url(self, raw_config):
        if hasattr(plugins, 'add_xivo_phonebook_url') and raw_config.get(u'config_version', 0) >= 1:
            plugins.add_xivo_phonebook_url(raw_config, u'snom')
        else:
            self._add_xivo_phonebook_url_compat(raw_config)

    def _add_xivo_phonebook_url_compat(self, raw_config):
        hostname = raw_config.get(u'X_xivo_phonebook_ip')
        if hostname:
            raw_config[u'XX_xivo_phonebook_url'] = u'http://{hostname}/service/ipbx/web_services.php/phonebook/search/'.format(hostname=hostname)

    def _check_config(self, raw_config):
        if u'http_port' not in raw_config:
            raise RawConfigError('only support configuration via HTTP')

    def _check_device(self, device):
        if u'mac' not in device:
            raise Exception('MAC address needed for device configuration')
        if u'model' not in device:
            raise Exception('Model name needed for device configuration')

    def _dev_specific_filename(self, device):
        return u'config.{}.xml'.format(format_mac(device[u'mac'], separator=''))

    def _add_server_url(self, raw_config):
        ip = raw_config[u'ip']
        http_port = raw_config[u'http_port']
        raw_config[u'XX_server_url'] = u'http://{}:{}'.format(ip, http_port)

    def configure(self, device, raw_config):
        self._check_config(raw_config)
        self._check_device(device)
        xml_filename = self._dev_specific_filename(device)

        # generate xml file
        tpl = self._tpl_helper.get_dev_template(xml_filename, device)

        model = device.get(u'model')
        self._update_sip_lines(raw_config)
        self._add_fkeys(raw_config, model)
        self._add_timezone(raw_config)
        self._add_user_dtmf_info(raw_config)
        self._add_xivo_phonebook_url(raw_config)
        self._add_server_url(raw_config)
        self._add_language(raw_config)
        raw_config[u'XX_options'] = device.get(u'options', {})

        path = os.path.join(self._tftpboot_dir, xml_filename)
        self._tpl_helper.dump(tpl, raw_config, path, self._ENCODING)

    def deconfigure(self, device):
        filename = self._dev_specific_filename(device)
        try:
            os.remove(os.path.join(self._tftpboot_dir, filename))
        except OSError as e:
            # ignore
            logger.warning('error while removing file: "%s"', e)

    if hasattr(synchronize, 'standard_sip_synchronize'):
        def synchronize(self, device, raw_config):
            return synchronize.standard_sip_synchronize(device, event='check-sync')

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
        if u'mac' not in device:
            return None

        return self._dev_specific_filename(device)

    def is_sensitive_filename(self, filename):
        return bool(self._SENSITIVE_FILENAME_REGEX.match(filename))
