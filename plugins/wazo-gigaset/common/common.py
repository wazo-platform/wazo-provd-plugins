# -*- coding: utf-8 -*-
# Copyright 2011-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+
"""Common code shared by the various wazo-gigaset plugins."""


import os
import logging
import re
from provd.devices.pgasso import BasePgAssociator, IMPROBABLE_SUPPORT,\
    COMPLETE_SUPPORT, UNKNOWN_SUPPORT
from provd.plugins import StandardPlugin, TemplatePluginHelper
from provd.util import norm_mac
from provd.servers.http import HTTPNoListingFileService
from twisted.internet import defer, threads

logger = logging.getLogger('plugin.wazo-gigaset')

VENDOR = u'Gigaset'


class GigasetDHCPDeviceInfoExtractor(object):
    _VDI = {
        'N720_DM_PRO':  u'N720 DM PRO',
        'N720_IP_PRO': u'N720 IP PRO',
        'N510_IP_PRO':  u'N510 IP PRO',
    }
    
    def extract(self, request, request_type):
        return defer.succeed(self._do_extract(request))
    
    def _do_extract(self, request):
        options = request[u'options']
        if 60 in options:
            return self._extract_from_vdi(options[60])
        else:
            return None
    
    def _extract_from_vdi(self, vdi):
        # Vendor class identifier:
        #   "Gigaset_N720_DM_PRO"
        #   "Gigaset_N720_IP_PRO"
        #   "Gigaset_N510_IP_PRO"
        vdi_to_check = '_'.join(vdi.split('_')[1:])
        if vdi_to_check in self._VDI:
            return {u'vendor': VENDOR,
                    u'model': self._VDI[vdi_to_check]}
        else:
            return None


class GigasetHTTPDeviceInfoExtractor(object):

    _UA_REGEX = re.compile(r'')
    _PATH_REGEX = re.compile(r'')

    def extract(self, request, request_type):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request):
        match = self._PATH_REGEX.match(request.path)
        if match:
            dev_info = {u'vendor': VENDOR}
            
            return dev_info

    def _extract_from_ua(self, ua):
        # HTTP User-Agent:
        # "Gigaset N720 DM PRO/70.089.00.000.000;7C2F80CA21E4"
        m = self._UA_REGEX.search(ua)
        if m:
            raw_model, raw_version = m.groups()
            return {u'vendor': VENDOR,
                    u'model': raw_model.decode('ascii'),
                    u'version': raw_version.decode('ascii')}
        return None):
        


class BaseGigasetPgAssociator(BasePgAssociator):
    def __init__(self, models):
        self._models = models
    
    def _do_associate(self, vendor, model, version):
        if vendor == VENDOR:
            if model in self._models:
                return COMPLETE_SUPPORT
            else:
                return UNKNOWN_SUPPORT
        else:
            return IMPROBABLE_SUPPORT



class BaseGigasetPlugin(StandardPlugin):
    _ENCODING = 'UTF-8'
    
    def __init__(self, app, plugin_dir, gen_cfg, spec_cfg):
        StandardPlugin.__init__(self, app, plugin_dir, gen_cfg, spec_cfg)
        self._app = app
        
        self._tpl_helper = TemplatePluginHelper(plugin_dir)
        
    dhcp_dev_info_extractor = GigasetDHCPDeviceInfoExtractor()
    http_dev_info_extractor = GigasetHTTPDeviceInfoExtractor()
    
    def _check_device(self, device):
        if u'ip' not in device:
            raise Exception('IP address needed for Gigaset configuration')
    
    def configure(self, device, raw_config):
        self._check_device(device)
        # nothing else to do
    
    def deconfigure(self, device):
        # nothing to do
        pass
    
    def _do_synchronize(self, device, raw_config):
        
    
    def synchronize(self, device, raw_config):
        assert u'ip' in device      # see self.configure() and plugin contract
        
        return threads.deferToThread(self._do_synchronize, device, raw_config)
