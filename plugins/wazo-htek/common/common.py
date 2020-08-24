# -*- coding: utf-8 -*-

# Copyright 2017-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import re
import os.path
from provd import plugins
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

logger = logging.getLogger('plugin.wazo-htek')


class BaseHtekHTTPDeviceInfoExtractor(object):
    _UA_REGEX_LIST = [
        re.compile(r'^Htek ([^ ]+) ([^ ]+) ([^ ]+)$')
    ]

    def extract(self, request, request_type):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request):
        ua = request.getHeader('User-Agent')
        if ua:
            return self._extract_from_ua(ua)

    def _extract_from_ua(self, ua):
        # HTTP User-Agent:
        #   "Htek UC903 2.0.4.2 00:1f:c1:1c:22:a9"

        for UA_REGEX in self._UA_REGEX_LIST:
            m = UA_REGEX.match(ua)
            if m:
                raw_model, raw_version, raw_mac = m.groups()
                try:
                    mac = norm_mac(raw_mac.decode('ascii'))
                except ValueError as e:
                    logger.warning('Could not normalize MAC address "%s": %s', raw_mac, e)
                    return {u'vendor': u'Htek',
                            u'model': raw_model.decode('ascii'),
                            u'version': raw_version.decode('ascii')}
                else:
                    return {u'vendor': u'Htek',
                            u'model': raw_model.decode('ascii'),
                            u'version': raw_version.decode('ascii'),
                            u'mac': mac}
        return None


class BaseHtekPgAssociator(BasePgAssociator):
    def __init__(self, model_versions):
        # model_versions is a dictionary which keys are model IDs and values
        # are version IDs.
        BasePgAssociator.__init__(self)
        self._model_versions = model_versions

    def _do_associate(self, vendor, model, version):
        if vendor == u'Htek':
            if model in self._model_versions:
                if version == self._model_versions[model]:
                    return FULL_SUPPORT
                return COMPLETE_SUPPORT
            return PROBABLE_SUPPORT
        return IMPROBABLE_SUPPORT


class BaseHtekPlugin(StandardPlugin):
    _ENCODING = 'UTF-8'
    _LOCALE = {
        u'de_DE': (u'German', u'Germany'),
        u'en_US': (u'English', u'United States'),
        u'en_GB': (u'English', u'Great Britain'),
        u'es_ES': (u'Spanish', u'Spain'),
        u'fr_FR': (u'French', u'France'),
        u'fr_CA': (u'French', u'United States'),
    }

    # Used for tone select
    _COUNTRIES = {
        'Custom': 0,
        'Australia': 1,
        'Austria': 2,
        'Brazil': 3,
        'Belgium': 4,
        'China': 5,
        'Chile': 6,
        'Czech': 7,
        'Denmark': 8,
        'Finland': 9,
        'France': 10,
        'Germany': 11,
        'Great Britain': 12,
        'Greece': 13,
        'Hungary': 14,
        'Lithuania': 15,
        'India': 16,
        'Italy': 17,
        'Japan': 18,
        'Mexico': 19,
        'New Zealand': 20,
        'Netherlands': 21,
        'Norway': 22,
        'Portugal': 23,
        'Spain': 24,
        'Switzerland': 25,
        'Sweden': 26,
        'Russia': 27,
        'United States': 28,
    }

    _SIP_DTMF_MODE = {
        u'RTP-out-of-band': u'0',
        u'RTP-in-band': u'1',
        u'SIP-INFO': u'2',
    }
    _SIP_TRANSPORT = {
        u'udp': u'0',
        u'tcp': u'1',
        u'tls': u'2',
    }
    _SIP_TRANSPORT_DEF = u'0'
    _NB_LINEKEYS = {
        u'UC926': 36,
        u'UC926E': 36,
        u'UC924': 28,
        u'UC924E': 28,
        u'UC923': 20,
        u'UC912': 12,
        u'UC912E': 12,
        u'UC912G': 12,
        u'UC903': 20,
        u'UC862': 14,
        u'UC860': 14,
        u'UC860P': 14,
        u'UC842': 4,
        u'UC840': 4,
        u'UC840P': 4,
        u'UC806': 4,
        u'UC806T': 4,
        u'UC804': 4,
        u'UC804T': 4,
        u'UC803': 0,
        u'UC803T': 0,
        u'UC802': 0,
        u'UC802T': 0,
    }

    _TZ_INFO = {
        (-11, 00): 105,
        (-10, 00): 2,
        (-9, 00): 3,
        (-8, 00): 6,
        (-7, 00): 10,
        (-6, 00): 14,
        (-5, 00): 18,
        (-4, 30): 19,
        (-4, 00): 20,
        (-3, 30): 26,
        (-3, 00): 30,
        (-2, 00): 31,
        (-1, 00): 32,
        (00, 00): 33,
        (1, 00): 49,
        (2, 00): 57,
        (3, 00): 73,
        (3, 30): 74,
        (4, 00): 77,
        (5, 00): 83,
        (5, 30): 84,
        (6, 00): 85,
        (7, 00): 88,
        (8, 00): 89,
        (9, 00): 93,
        (9, 30): 94,
        (10, 00): 96,
        (10, 30): 100,
        (11, 00): 101,
        (12, 00): 102,
        (12, 45): 103,
        (13, 00): 104,
    }

    def __init__(self, app, plugin_dir, gen_cfg, spec_cfg):
        StandardPlugin.__init__(self, app, plugin_dir, gen_cfg, spec_cfg)

        self._tpl_helper = TemplatePluginHelper(plugin_dir)

        downloaders = FetchfwPluginHelper.new_downloaders(gen_cfg.get('proxies'))
        fetchfw_helper = FetchfwPluginHelper(plugin_dir, downloaders)

        self.services = fetchfw_helper.services()
        self.http_service = HTTPNoListingFileService(self._tftpboot_dir)

    http_dev_info_extractor = BaseHtekHTTPDeviceInfoExtractor()

    def configure_common(self, raw_config):
        for filename, tpl_filename in self._COMMON_FILES:
            tpl = self._tpl_helper.get_template('common/%s' % tpl_filename)
            dst = os.path.join(self._tftpboot_dir, filename)
            self._tpl_helper.dump(tpl, raw_config, dst, self._ENCODING)

    def _update_sip_lines(self, raw_config):
        for line_no, line in raw_config[u'sip_lines'].iteritems():
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

    def _gen_param_num(self, line, offset=0):
        '''Method that generates line parameter numbers for the config file

        There are several steps in the numbering of parameters that need to
        be supported.'''
        param_nb = 0
        mode_nb = 0
        limit_step1 = 5
        limit_step2 = 37
        mode_base = 20600
        param_step1_base = 41200
        param_step2_base = 20200
        param_step3_base = 23000
        line = int(line)
        if line < limit_step1:
            param_nb = param_step1_base + line - 1 + 100 * offset
            mode_nb = mode_base + line - 1
        elif line >= limit_step1 and line < limit_step2:
            param_nb = param_step2_base + offset + 5 * (line - limit_step1)
            mode_nb = mode_base + line - 1
        else:
            param_nb = param_step3_base + offset + 5 * (line - limit_step2)
            mode_nb = param_nb
        return param_nb, mode_nb

    def _add_fkeys(self, device, raw_config):
        # Setting up the line/function keys
        complete_fkeys = {}
        fkeys = raw_config[u'funckeys']
        fkey_type_assoc = {u'': 0, u'speeddial': 2, u'blf': 3, u'park': 8}

        if u'model' in device and device[u'model'] is not None and device[u'model'] in self._NB_LINEKEYS:
            for key_nb in range(1, self._NB_LINEKEYS[device[u'model']] + 1):
                if str(key_nb) in raw_config[u'sip_lines']:
                    sip_line = raw_config[u'sip_lines'][str(key_nb)]
                    val = {u'type': 1, u'value': '', u'label': sip_line['number']}
                else:
                    val = fkeys.get(str(key_nb), {u'type': '', u'value': '', u'label': ''})
                    val[u'type'] = fkey_type_assoc[val[u'type']]
                complete_fkeys[key_nb] = {
                    'type': {'p_nb': self._gen_param_num(key_nb)[0], 'val': val[u'type']},
                    'mode': {'p_nb': self._gen_param_num(key_nb)[1]},
                    'value': {'p_nb': self._gen_param_num(key_nb, offset=1)[0], 'val': val[u'value']},
                    'label': {'p_nb': self._gen_param_num(key_nb, offset=2)[0], 'val': val[u'label']},
                    'account': {'p_nb': self._gen_param_num(key_nb, offset=3)[0]},
                    'extension': {'p_nb': self._gen_param_num(key_nb, offset=4)[0], 'val': val[u'value']},
                }
            raw_config[u'XX_fkeys'] = complete_fkeys

    def _add_country_and_lang(self, raw_config):
        locale = raw_config.get(u'locale')
        if locale in self._LOCALE:
            (lang, country) = self._LOCALE[locale]
            (raw_config[u'XX_lang'],
             raw_config[u'XX_country']) = (lang, self._COUNTRIES[country])

    def _add_timezone(self, raw_config):
        timezone = raw_config.get(u'timezone', 'Etc/UTC')
        tz_db = tzinform.TextTimezoneInfoDB()
        tz_timezone_info = tz_db.get_timezone_info(timezone)
        tz_info = tz_timezone_info['utcoffset'].as_hms
        offset_hour = tz_info[0]
        offset_minutes = tz_info[1]

        if (offset_hour, offset_minutes) in self._TZ_INFO:
            raw_config[u'XX_timezone_code'] = self._TZ_INFO[(offset_hour, offset_minutes)]
        else:
            raw_config[u'XX_timezone_code'] = self._TZ_INFO[(-5, 0)]

    def _add_sip_transport(self, raw_config):
        raw_config[u'XX_sip_transport'] = self._SIP_TRANSPORT.get(raw_config.get(u'sip_transport'),
                                                                  self._SIP_TRANSPORT_DEF)

    def _add_xivo_phonebook_url(self, raw_config):
        if hasattr(plugins, 'add_xivo_phonebook_url') and raw_config.get(u'config_version', 0) >= 1:
            plugins.add_xivo_phonebook_url(raw_config, u'htek', entry_point=u'lookup')
        else:
            self._add_xivo_phonebook_url_compat(raw_config)

    def _add_xivo_phonebook_url_compat(self, raw_config):
        hostname = raw_config.get(u'X_xivo_phonebook_ip')
        if hostname:
            raw_config[u'XX_xivo_phonebook_url'] = u'http://{hostname}/service/ipbx/web_services.php/phonebook/search/?name=#SEARCH'.format(hostname=hostname)

    _SENSITIVE_FILENAME_REGEX = re.compile(r'^cfg[0-9a-f]{12}\.xml')

    def _dev_specific_filename(self, device):
        # Return the device specific filename (not pathname) of device
        fmted_mac = format_mac(device[u'mac'], separator='')
        return 'cfg' + fmted_mac + '.xml'

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

        self._add_fkeys(device, raw_config)
        self._add_country_and_lang(raw_config)
        self._add_timezone(raw_config)
        self._add_sip_transport(raw_config)
        self._update_sip_lines(raw_config)
        self._add_xivo_phonebook_url(raw_config)
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
                    return threads.deferToThread(sync_service.sip_notify, ip, 'check-sync')

    def get_remote_state_trigger_filename(self, device):
        if u'mac' not in device:
            return None

        return self._dev_specific_filename(device)

    def is_sensitive_filename(self, filename):
        return bool(self._SENSITIVE_FILENAME_REGEX.match(filename))
