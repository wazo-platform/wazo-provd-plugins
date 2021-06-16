# -*- coding: utf-8 -*-

# Copyright 2010-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import re
import os.path
from provd import synchronize
from provd.devices.config import RawConfigError
from provd.plugins import FetchfwPluginHelper, StandardPlugin, TemplatePluginHelper
from provd.devices.pgasso import (
    BasePgAssociator,
    COMPLETE_SUPPORT,
    FULL_SUPPORT,
    IMPROBABLE_SUPPORT,
    UNKNOWN_SUPPORT,
)
from provd.servers.http import HTTPNoListingFileService
from provd.util import format_mac, norm_mac
from twisted.internet import defer, threads

logger = logging.getLogger('plugin.wazo-grandstream')

TZ_NAME = {'Europe/Paris': 'CET-1CEST-2,M3.5.0/02:00:00,M10.5.0/03:00:00'}
LOCALE = {
    u'de_DE': 'de',
    u'es_ES': 'es',
    u'fr_FR': 'fr',
    u'fr_CA': 'fr',
    u'it_IT': 'it',
    u'nl_NL': 'nl',
    u'en_US': 'en',
}

FUNCKEY_TYPES = {
    u'speeddial': 0,
    u'blf': 1,
    u'park': 9,
    u'default': 31,
    u'disabled': -1,
}


class BaseGrandstreamHTTPDeviceInfoExtractor(object):

    # Grandstream Model HW GXP1405 SW 1.0.4.23 DevId 000b8240d55c
    # Grandstream Model HW GXP1628 SW 1.0.4.138 DevId c074ad2bd859
    # Grandstream Model HW GXP2200 V2.2A SW 1.0.1.33 DevId 000b82462d97
    # Grandstream Model HW GXV3240 V1.6B SW 1.0.1.27 DevId 000b82632815
    # Grandstream Model HW GXV3350  V1.3A SW 1.0.1.8 DevId c074ad150b88
    # Grandstream GXP2000 (gxp2000e.bin:1.2.5.3/boot55e.bin:1.1.6.9) DevId 000b822726c8
    # Grandstream Model HW GRP2614 SW 1.0.5.15 DevId c074ad0b63ee
    # Grandstream Model HW HT801 V1.1A SW 1.0.17.5 DevId c074ad273a10

    _UA_REGEX_LIST = [
        re.compile(
            r'^Grandstream Model HW (\w+)(?:\s+V[^ ]+)? SW ([^ ]+) DevId ([^ ]+)'
        ),
        re.compile(r'^Grandstream (GXP2000) .*:([^ ]+)\) DevId ([^ ]+)'),
    ]

    def extract(self, request, request_type):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request):
        ua = request.getHeader('User-Agent')
        if ua:
            return self._extract_from_ua(ua)

    def _extract_from_ua(self, ua):
        for UA_REGEX in self._UA_REGEX_LIST:
            m = UA_REGEX.match(ua)
            if m:
                raw_model, raw_version, raw_mac = m.groups()
                try:
                    mac = norm_mac(raw_mac.decode('ascii'))
                except ValueError as e:
                    logger.warning(
                        'Could not normalize MAC address "%s": %s', raw_mac, e
                    )
                else:
                    return {
                        u'vendor': u'Grandstream',
                        u'model': raw_model.decode('ascii'),
                        u'version': raw_version.decode('ascii'),
                        u'mac': mac,
                    }


class BaseGrandstreamPgAssociator(BasePgAssociator):
    def __init__(self, models, version):
        BasePgAssociator.__init__(self)
        self._models = models
        self._version = version

    def _do_associate(self, vendor, model, version):
        if vendor == u'Grandstream':
            if model in self._models:
                if version.startswith(self._version):
                    return FULL_SUPPORT
                return COMPLETE_SUPPORT
            return UNKNOWN_SUPPORT
        return IMPROBABLE_SUPPORT


class BaseGrandstreamPlugin(StandardPlugin):
    _ENCODING = 'UTF-8'
    # VPKs are the virtual phone keys on the main display
    # MPKs are the physical programmable keys on some models
    MODEL_FKEYS = {
        u'GRP2612': {
            u'vpk': 16,
            u'mpk': 0,
        },
        u'GRP2613': {
            u'vpk': 24,
            u'mpk': 0,
        },
        u'GRP2614': {
            u'vpk': 16,
            u'mpk': 24,
        },
        u'GRP2615': {
            u'vpk': 40,
            u'mpk': 0,
        },
        u'GRP2616': {
            u'vpk': 16,
            u'mpk': 24,
        },
    }

    DTMF_MODES = {
        # mode: (in audio, in RTP, in SIP)
        u'RTP-in-band': ('Yes', 'Yes', 'No'),
        u'RTP-out-of-band': ('No', 'Yes', 'No'),
        u'SIP-INFO': ('No', 'No', 'Yes'),
    }

    SIP_TRANSPORTS = {
        u'udp': u'UDP',
        u'tcp': u'TCP',
        u'tls': u'TlsOrTcp',
    }

    def __init__(self, app, plugin_dir, gen_cfg, spec_cfg):
        StandardPlugin.__init__(self, app, plugin_dir, gen_cfg, spec_cfg)
        # update to use the non-standard tftpboot directory
        self._base_tftpboot_dir = self._tftpboot_dir
        self._tftpboot_dir = os.path.join(self._tftpboot_dir, 'Grandstream')

        self._tpl_helper = TemplatePluginHelper(plugin_dir)

        downloaders = FetchfwPluginHelper.new_downloaders(gen_cfg.get('proxies'))
        fetchfw_helper = FetchfwPluginHelper(plugin_dir, downloaders)
        # update to use the non-standard tftpboot directory
        fetchfw_helper.root_dir = self._tftpboot_dir

        self.services = fetchfw_helper.services()
        self.http_service = HTTPNoListingFileService(self._base_tftpboot_dir)

    http_dev_info_extractor = BaseGrandstreamHTTPDeviceInfoExtractor()

    def _dev_specific_filename(self, device):
        # Return the device specific filename (not pathname) of device
        fmted_mac = format_mac(device[u'mac'], separator='', uppercase=False)
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
        self._check_lines_password(raw_config)
        self._add_sip_transport(raw_config)
        self._add_timezone(raw_config)
        self._add_locale(raw_config)
        self._add_dtmf_mode(raw_config)
        self._add_fkeys(raw_config)
        self._add_mpk(raw_config)
        self._add_v2_fkeys(raw_config, device.get(u'model'))
        self._add_dns(raw_config)
        filename = self._dev_specific_filename(device)
        tpl = self._tpl_helper.get_dev_template(filename, device)

        path = os.path.join(self._tftpboot_dir, filename)
        self._tpl_helper.dump(tpl, raw_config, path, self._ENCODING)

    def deconfigure(self, device):
        self._remove_configuration_file(device)

    def _remove_configuration_file(self, device):
        path = os.path.join(self._tftpboot_dir, self._dev_specific_filename(device))
        try:
            os.remove(path)
        except OSError as e:
            logger.info('error while removing configuration file: %s', e)

    if hasattr(synchronize, 'standard_sip_synchronize'):

        def synchronize(self, device, raw_config):
            return synchronize.standard_sip_synchronize(device)

    else:
        # backward compatibility with older wazo-provd server
        def synchronize(self, device, raw_config):
            try:
                ip = device[u'ip'].encode('ascii')
            except KeyError:
                return defer.fail(
                    Exception('IP address needed for device synchronization')
                )
            else:
                sync_service = synchronize.get_sync_service()
                if sync_service is None or sync_service.TYPE != 'AsteriskAMI':
                    return defer.fail(
                        Exception('Incompatible sync service: %s' % sync_service)
                    )
                else:
                    return threads.deferToThread(
                        sync_service.sip_notify, ip, 'check-sync'
                    )

    def get_remote_state_trigger_filename(self, device):
        if u'mac' in device:
            return self._dev_specific_filename(device)

    def _check_lines_password(self, raw_config):
        for line in raw_config[u'sip_lines'].itervalues():
            if line[u'password'] == u'autoprov':
                line[u'password'] = u''

    def _add_timezone(self, raw_config):
        if u'timezone' in raw_config and raw_config[u'timezone'] in TZ_NAME:
            raw_config[u'XX_timezone'] = TZ_NAME[raw_config[u'timezone']]
        else:
            raw_config['timezone'] = TZ_NAME['Europe/Paris']

    def _add_locale(self, raw_config):
        locale = raw_config.get(u'locale')
        if locale in LOCALE:
            raw_config[u'XX_locale'] = LOCALE[locale]

    def _add_fkeys(self, raw_config):
        lines = []
        for funckey_no, funckey_dict in raw_config[u'funckeys'].iteritems():
            i_funckey_no = int(funckey_no)
            funckey_type = funckey_dict[u'type']
            if funckey_type not in FUNCKEY_TYPES:
                logger.info('Unsupported funckey type: %s', funckey_type)
                continue
            type_code = u'P32%s' % (i_funckey_no + 2)
            lines.append((type_code, FUNCKEY_TYPES[funckey_type]))
            line_code = self._format_code(3 * i_funckey_no - 2)
            lines.append((line_code, int(funckey_dict[u'line']) - 1))
            if u'label' in funckey_dict:
                label_code = self._format_code(3 * i_funckey_no - 1)
                lines.append((label_code, funckey_dict[u'label']))
            value_code = self._format_code(3 * i_funckey_no)
            lines.append((value_code, funckey_dict[u'value']))
        raw_config[u'XX_fkeys'] = lines

    def _add_mpk(self, raw_config):
        lines = []
        start_code = 23000
        for funckey_no, funckey_dict in raw_config[u'funckeys'].iteritems():
            i_funckey_no = int(funckey_no)  # starts at 1
            funckey_type = funckey_dict[u'type']
            if funckey_type not in FUNCKEY_TYPES:
                logger.info('Unsupported funckey type: %s', funckey_type)
                continue
            start_p_code = start_code + (i_funckey_no - 1) * 5
            type_code = u'P{}'.format(start_p_code)
            lines.append((type_code, FUNCKEY_TYPES[funckey_type]))
            line_code = u'P{}'.format(start_p_code + 1)
            lines.append((line_code, int(funckey_dict[u'line']) - 1))
            if u'label' in funckey_dict:
                label_code = u'P{}'.format(start_p_code + 2)
                lines.append((label_code, funckey_dict[u'label']))
            value_code = u'P{}'.format(start_p_code + 3)
            lines.append((value_code, funckey_dict[u'value']))
        raw_config[u'XX_mpk'] = lines

    def _add_v2_fkeys(self, raw_config, model):
        lines = []
        model_fkeys = self.MODEL_FKEYS.get(model)
        if not model_fkeys:
            logger.info('Unknown model: "%s"', model)
            return
        for funckey_no in range(1, model_fkeys[u'vpk'] + 1):
            funckey = raw_config[u'funckeys'].get(str(funckey_no), {})
            funckey_type = funckey.get(u'type', 'disabled')
            if funckey_type not in FUNCKEY_TYPES:
                logger.info('Unsupported funckey type: %s', funckey_type)
                continue
            if str(funckey_no) in raw_config[u'sip_lines']:
                logger.info(
                    'Function key %s would conflict with an existing line', funckey_no
                )
                continue
            lines.append(
                (
                    funckey_no,
                    {
                        u'section': u'vpk',
                        u'type': FUNCKEY_TYPES[funckey_type],
                        u'label': funckey.get(u'label') or u'',
                        u'value': funckey.get(u'value') or u'',
                    },
                )
            )
        for funckey_no in range(1, model_fkeys[u'mpk'] + 1):
            funckey = raw_config[u'funckeys'].get(
                str(funckey_no + model_fkeys[u'vpk']), {}
            )
            funckey_type = funckey.get(u'type', 'disabled')
            if funckey_type not in FUNCKEY_TYPES:
                logger.info('Unsupported funckey type: %s', funckey_type)
            lines.append(
                (
                    funckey_no,
                    {
                        u'section': u'mpk',
                        u'type': FUNCKEY_TYPES[funckey_type],
                        u'label': funckey.get(u'label') or u'',
                        u'value': funckey.get(u'value') or u'',
                    },
                )
            )
        raw_config[u'XX_v2_fkeys'] = lines

    def _format_code(self, code):
        if code >= 10:
            str_code = str(code)
        else:
            str_code = u'0%s' % code
        return u'P3%s' % str_code

    def _add_dns(self, raw_config):
        if raw_config.get(u'dns_enabled'):
            dns_parts = raw_config[u'dns_ip'].split('.')
            for part_nb, part in enumerate(dns_parts, start=1):
                raw_config[u'XX_dns_%s' % part_nb] = part

    def _add_dtmf_mode(self, raw_config):
        if raw_config.get(u'sip_dtmf_mode'):
            dtmf_info = self.DTMF_MODES[raw_config[u'sip_dtmf_mode']]
            raw_config['XX_dtmf_in_audio'] = dtmf_info[0]
            raw_config['XX_dtmf_in_rtp'] = dtmf_info[1]
            raw_config['XX_dtmf_in_sip'] = dtmf_info[2]

    def _add_sip_transport(self, raw_config):
        sip_transport = raw_config.get(u'sip_transport')
        if sip_transport in self.SIP_TRANSPORTS:
            raw_config[u'XX_sip_transport'] = self.SIP_TRANSPORTS[sip_transport]
