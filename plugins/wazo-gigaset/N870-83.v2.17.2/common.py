# -*- coding: utf-8 -*-
# Copyright 2011-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

"""Common code shared by the various wazo-gigaset plugins."""

import os
import logging
import re
import datetime
import time
from provd.devices.pgasso import BasePgAssociator, IMPROBABLE_SUPPORT,\
    COMPLETE_SUPPORT, FULL_SUPPORT, UNKNOWN_SUPPORT
from provd.plugins import StandardPlugin, TemplatePluginHelper, FetchfwPluginHelper
from provd.util import norm_mac, format_mac
from provd import synchronize
from provd import plugins
from provd.servers.http import HTTPNoListingFileService
from twisted.internet import defer

logger = logging.getLogger('plugin.wazo-gigaset')

VENDOR = u'Gigaset'


class GigasetHTTPDeviceInfoExtractor(object):

    _UA_REGEX = re.compile(r'^(Gigaset )?(?P<model>[\w\s]+)\/(?P<version>(?:\w{2,3}\.){3,4}\w{1,3})(?:\+.+)?;(?P<mac>[0-9A-F]{12})?$')

    def extract(self, request, request_type):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request):
        dev_info = {}

        ua = request.getHeader('User-Agent')
        if ua:
            dev_info.update(self._extract_from_ua(ua))

        return dev_info

    def _extract_from_ua(self, ua):
        # HTTP User-Agent:
        # "Gigaset N870 IP PRO/83.V2.11.0+build.a546b91;7C2F80E0D605"
        m = self._UA_REGEX.search(ua)
        dev_info = {}
        if m:
            dev_info = {u'vendor': VENDOR,
                        u'model': m.group('model').decode('ascii'),
                        u'version': m.group('version').decode('ascii')}
            if 'mac' in m.groupdict():
                dev_info[u'mac'] = norm_mac(m.group('mac').decode('ascii'))

        return dev_info


class BaseGigasetPgAssociator(BasePgAssociator):
    def __init__(self, models):
        self._models = models

    def _do_associate(self, vendor, model, version):
        if vendor == VENDOR:
            if model in self._models:
                if version == self._models[model]:
                    return FULL_SUPPORT
                return COMPLETE_SUPPORT
            else:
                return UNKNOWN_SUPPORT
        else:
            return IMPROBABLE_SUPPORT


class BaseGigasetPlugin(StandardPlugin):
    _ENCODING = 'UTF-8'

    _SIP_DTMF_MODE = {
        u'RTP-in-band': u'1',
        u'RTP-out-of-band': u'2',
        u'SIP-INFO': u'4',
    }
    _SIP_SRTP_MODE = {
        u'disabled': u'0',
        u'preferred': u'1',
        u'required': u'1',
    }
    _SIP_TRANSPORT = {
        u'udp': u'1',
        u'tcp': u'2',
        u'tls': u'3',
    }

    def __init__(self, app, plugin_dir, gen_cfg, spec_cfg):
        StandardPlugin.__init__(self, app, plugin_dir, gen_cfg, spec_cfg)
        self._app = app

        self._tpl_helper = TemplatePluginHelper(plugin_dir)
        downloaders = FetchfwPluginHelper.new_downloaders(gen_cfg.get('proxies'))
        fetchfw_helper = FetchfwPluginHelper(plugin_dir, downloaders)

        self.services = fetchfw_helper.services()
        self.http_service = HTTPNoListingFileService(self._tftpboot_dir)

    http_dev_info_extractor = GigasetHTTPDeviceInfoExtractor()

    def _check_device(self, device):
        if u'ip' not in device:
            raise Exception('IP address needed for Gigaset configuration')

    def _dev_specific_filename(self, device):
        # Return the device specific filename (not pathname) of device
        fmted_mac = format_mac(device[u'mac'], separator='', uppercase=False)
        return fmted_mac + '.xml'

    def _add_phonebook(self, raw_config):
        uuid_format = u'{scheme}://{hostname}:{port}/0.1/directories/lookup/{profile}/gigaset/{user_uuid}?'
        plugins.add_xivo_phonebook_url_from_format(raw_config, uuid_format)

    def _add_xx_vars(self, device, raw_config):
        raw_config[u'XX_mac_addr'] = format_mac(device[u'mac'], separator='', uppercase=True)

        cur_datetime = datetime.datetime.now()
        raw_config[u'XX_version_date'] = cur_datetime.strftime('%d%m%y%H%M')

        raw_config[u'XX_epoch'] = int(time.time())

    def _add_voip_providers(self, raw_config):
        voip_providers = dict()
        provider_id = 0
        sip_lines = raw_config.get(u'sip_lines')
        dtmf_mode = raw_config.get(u'sip_dtmf_mode', '1')
        srtp_mode = raw_config.get(u'sip_srtp_mode', '0')
        sip_transport = self._SIP_TRANSPORT.get(raw_config.get(u'sip_transport', '1'))
        if sip_lines:
            for line in sip_lines.itervalues():
                proxy_ip = line.get(u'proxy_ip')
                proxy_port = line.get(u'proxy_port', 5060)
                line_dtmf_mode = self._SIP_DTMF_MODE.get(line.get(u'dtmf_mode', dtmf_mode))
                line_srtp_mode = self._SIP_SRTP_MODE.get(line.get(u'strp_mode', srtp_mode))
                if (proxy_ip, proxy_port) not in voip_providers:
                    provider = {
                        u'id': provider_id,
                        u'sip_proxy_ip': proxy_ip,
                        u'sip_proxy_port': proxy_port,
                        u'dtmf_mode': line_dtmf_mode,
                        u'srtp_mode': line_srtp_mode,
                        u'sip_transport': sip_transport,
                    }
                    line[u'provider_id'] = provider_id
                    voip_providers[(proxy_ip, proxy_port)] = provider
                    provider_id += 1
                else:
                    line[u'provider_id'] = voip_providers[(proxy_ip, proxy_port)]['id']

        raw_config[u'XX_voip_providers'] = voip_providers.values()

    def _add_ac_code(self, raw_config):
        sip_lines = raw_config.get(u'sip_lines')
        if sip_lines:
            for line in sip_lines.itervalues():
                number = line.get(u'number')
                if number.startswith(u'auto'):
                    line[u'XX_hs_code'] = '0000'
                else:
                    line[u'XX_hs_code'] = number[-4:].zfill(4)

    def configure(self, device, raw_config):
        self._check_device(device)
        filename = self._dev_specific_filename(device)
        tpl = self._tpl_helper.get_dev_template(filename, device)

        self._add_voip_providers(raw_config)
        self._add_ac_code(raw_config)
        self._add_xx_vars(device, raw_config)
        self._add_phonebook(raw_config)

        path = os.path.join(self._tftpboot_dir, filename)
        self._tpl_helper.dump(tpl, raw_config, path, self._ENCODING)

    def deconfigure(self, device):
        path = os.path.join(self._tftpboot_dir, self._dev_specific_filename(device))
        try:
            os.remove(path)
        except OSError as e:
            logger.info('error while removing configuration file: %s', e)

    def is_sensitive_filename(self, filename):
        return bool(self._SENSITIVE_FILENAME_REGEX.match(filename))

    _SENSITIVE_FILENAME_REGEX = re.compile(r'^[0-9a-f]{12}\.xml$')

    def synchronize(self, device, raw_config):
        return synchronize.standard_sip_synchronize(device)
