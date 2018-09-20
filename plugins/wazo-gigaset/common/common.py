# -*- coding: utf-8 -*-
# Copyright 2011-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

"""Common code shared by the various wazo-gigaset plugins."""

import os
import logging
import re
from provd.devices.pgasso import BasePgAssociator, IMPROBABLE_SUPPORT,\
    COMPLETE_SUPPORT, FULL_SUPPORT, UNKNOWN_SUPPORT
from provd.plugins import StandardPlugin, TemplatePluginHelper, FetchfwPluginHelper
from provd.util import norm_mac, format_mac
from provd import synchronize
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

    _UA_REGEX = re.compile(r'^(Gigaset )?(?P<model>N\d{3} .+)\/(?P<version>\d{2,3}\.\d{2,3})\.(\d{2,3})\.(\d{2,3})\.(\d{2,3});?(?P<mac>[A-F0-9]{12})?$')
    _PATH_REGEX = re.compile(r'^/\d{2}/\d{1}/(.+)$')

    def extract(self, request, request_type):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request):
        match = self._PATH_REGEX.search(request.path)
        if match:
            dev_info = {u'vendor': VENDOR}
            ua = request.getHeader('User-Agent')
            if ua:
                dev_info.update(self._extract_from_ua(ua))
            return dev_info

    def _extract_from_ua(self, ua):
        # HTTP User-Agent:
        # "Gigaset N720 DM PRO/70.089.00.000.000;7C2F80CA21E4"
        # "Gigaset N720 DM PRO/70.108.00.000.000"
        # "N510 IP PRO/42.242.00.000.000"
        m = self._UA_REGEX.search(ua)
        dev_info = None
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
    
    def __init__(self, app, plugin_dir, gen_cfg, spec_cfg):
        StandardPlugin.__init__(self, app, plugin_dir, gen_cfg, spec_cfg)
        self._app = app
        
        self._tpl_helper = TemplatePluginHelper(plugin_dir)
        downloaders = FetchfwPluginHelper.new_downloaders(gen_cfg.get('proxies'))
        fetchfw_helper = FetchfwPluginHelper(plugin_dir, downloaders)

        self.services = fetchfw_helper.services()
        self.http_service = HTTPNoListingFileService(self._tftpboot_dir)
        
    dhcp_dev_info_extractor = GigasetDHCPDeviceInfoExtractor()
    http_dev_info_extractor = GigasetHTTPDeviceInfoExtractor()
    
    def _check_device(self, device):
        if u'ip' not in device:
            raise Exception('IP address needed for Gigaset configuration')
    
    def _check_config(self, raw_config):
        pass

    def _dev_specific_filename(self, device):
        # Return the device specific filename (not pathname) of device
        fmted_mac = format_mac(device[u'mac'], separator='', uppercase=False)
        return fmted_mac + '.xml'

    def configure(self, device, raw_config):
        self._check_config(raw_config)
        self._check_device(device)
        filename = self._dev_specific_filename(device)
        tpl = self._tpl_helper.get_dev_template(filename, device)
        
        path = os.path.join(self._tftpboot_dir, filename)
        self._tpl_helper.dump(tpl, raw_config, path, self._ENCODING)
    
    def deconfigure(self, device):
        path = os.path.join(self._tftpboot_dir, self._dev_specific_filename(device))
        try:
            os.remove(path)
        except OSError as e:
            logger.info('error while removing configuration file: %s', e)

    def _do_synchronize(self, device, raw_config):
        return synchronize.standard_sip_synchronize(device)
    
    def synchronize(self, device, raw_config):
        assert u'ip' in device      # see self.configure() and plugin contract
        
        return threads.deferToThread(self._do_synchronize, device, raw_config)
