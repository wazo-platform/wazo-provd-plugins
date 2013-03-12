# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
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

"""Common plugin code shared by the various xivo-cisco-sip plugins."""

# TODO complete...

import logging
import os
from provd import synchronize
from provd import tzinform
from provd.devices.config import RawConfigError
from provd.plugins import StandardPlugin, FetchfwPluginHelper,\
    TemplatePluginHelper
from provd.servers.tftp.service import TFTPFileService
from provd.services import PersistentConfigureServiceDecorator,\
    JsonConfigPersister
from provd.util import format_mac
from twisted.internet import defer, threads

logger = logging.getLogger('plugin.xivo-cisco')

common = {}
execfile_('common.py', common)


class BaseCiscoSipPlugin(StandardPlugin):
    _ENCODING = 'UTF-8'
    _LOCALE = {
        # <locale>: (<name>, <lang code>, <network locale>)
        u'de_DE': (u'german_germany', u'de', u'germany'),
        u'en_US': (u'english_united_states', u'en', u'united_states'),
        u'es_ES': (u'spanish_spain', u'es', u'spain'),
        u'fr_FR': (u'french_france', u'fr', u'france'),
        u'fr_CA': (u'french_france', u'fr', u'canada')
    }
    
    def __init__(self, app, plugin_dir, gen_cfg, spec_cfg):
        StandardPlugin.__init__(self, app, plugin_dir, gen_cfg, spec_cfg)
        
        self._tpl_helper = TemplatePluginHelper(plugin_dir)
        
        handlers = FetchfwPluginHelper.new_handlers(gen_cfg.get('proxies'))
        downloaders = FetchfwPluginHelper.new_downloaders_from_handlers(handlers)
        cisco_dler = common['CiscoDownloader'](handlers)
        downloaders['x-cisco'] = cisco_dler
        fetchfw_helper = FetchfwPluginHelper(plugin_dir, downloaders)
        
        cfg_service = common['CiscoConfigureService'](cisco_dler, spec_cfg.get('username'),
                                                      spec_cfg.get('password'))
        persister = JsonConfigPersister(os.path.join(self._plugin_dir, 'var',
                                                     'config.json'))
        cfg_service = PersistentConfigureServiceDecorator(cfg_service, persister)
        
        self.services = {'configure': cfg_service,
                         'install': fetchfw_helper}
        self.tftp_service = TFTPFileService(self._tftpboot_dir)
    
    dhcp_dev_info_extractor = common['BaseCiscoDHCPDeviceInfoExtractor']()
    
    tftp_dev_info_extractor = common['BaseCiscoTFTPDeviceInfoExtractor']() 
    
    def _dev_specific_filename(self, device):
        # Return the device specific filename (not pathname) of device
        fmted_mac = format_mac(device[u'mac'], separator='', uppercase=True)
        return 'SEP%s.cfg.xml' % fmted_mac
    
    def _check_config(self, raw_config):
        if u'tftp_port' not in raw_config:
            raise RawConfigError('only support configuration via TFTP')
    
    def _check_device(self, device):
        if u'mac' not in device:
            raise Exception('MAC address needed for device configuration')
    
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
        except OSError, e:
            # ignore
            logger.info('error while removing file: %s', e)
