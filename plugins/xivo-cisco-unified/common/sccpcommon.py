# -*- coding: utf-8 -*-

# Copyright (C) 2010-2013 Avencall
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

"""Common plugin code shared by the various xivo-cisco-sccp plugins.

Support most of the 6900 and 7900 phones.

"""


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



class BaseCiscoSccpPlugin(StandardPlugin):
    # XXX actually, we didn't find which encoding Cisco SCCP are using
    _ENCODING = 'UTF-8'
    _TZ_MAP = common['_gen_tz_map']()
    _TZ_VALUE_DEF = u'Eastern Standard/Daylight Time'
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

        downloaders = FetchfwPluginHelper.new_downloaders(gen_cfg.get('proxies'))
        fetchfw_helper = FetchfwPluginHelper(plugin_dir, downloaders)

        self.services = fetchfw_helper.services()
        self.tftp_service = TFTPFileService(self._tftpboot_dir)
    
    dhcp_dev_info_extractor = common['BaseCiscoDHCPDeviceInfoExtractor']()
    
    tftp_dev_info_extractor = common['BaseCiscoTFTPDeviceInfoExtractor']() 
    
    def _add_locale(self, raw_config):
        locale = raw_config.get(u'locale')
        if locale in self._LOCALE:
            raw_config[u'XX_locale'] = self._LOCALE[locale]
    
    def _tzinfo_to_value(self, tzinfo):
        utcoffset_m = tzinfo['utcoffset'].as_minutes
        if utcoffset_m not in self._TZ_MAP:
            # No UTC offset matching. Let's try finding one relatively close...
            for supp_offset in [30, -30, 60, -60]:
                if utcoffset_m + supp_offset in self._TZ_MAP:
                    utcoffset_m += supp_offset
                    break
            else:
                return self._TZ_VALUE_DEF
        
        dst_map = self._TZ_MAP[utcoffset_m]
        if tzinfo['dst']:
            dst_key = tzinfo['dst']['as_string']
        else:
            dst_key = None
        if dst_key not in dst_map:
            # No DST rules matching. Fallback on all-standard time or random
            # DST rule in last resort...
            if None in dst_map:
                dst_key = None
            else:
                dst_key = dst_map.keys[0]
        return dst_map[dst_key]
    
    def _add_timezone(self, raw_config):
        raw_config[u'XX_timezone'] = self._TZ_VALUE_DEF
        if u'timezone' in raw_config:
            try:
                tzinfo = tzinform.get_timezone_info(raw_config[u'timezone'])
            except tzinform.TimezoneNotFoundError, e:
                logger.info('Unknown timezone: %s', e)
            else:
                raw_config[u'XX_timezone'] = self._tzinfo_to_value(tzinfo)
    
    def _update_call_managers(self, raw_config):
        for priority, call_manager in raw_config[u'sccp_call_managers'].iteritems():
            call_manager[u'XX_priority'] = unicode(int(priority) - 1)
    
    def _dev_specific_filename(self, device):
        # Return the device specific filename (not pathname) of device
        fmted_mac = format_mac(device[u'mac'], separator='', uppercase=True)
        return 'SEP%s.cnf.xml' % fmted_mac
    
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
        
        # TODO check support for addons, and test what the addOnModules is
        #      really doing...
        raw_config[u'XX_addons'] = ''
        self._add_locale(raw_config)
        self._add_timezone(raw_config)
        self._update_call_managers(raw_config)
        
        path = os.path.join(self._tftpboot_dir, filename)
        self._tpl_helper.dump(tpl, raw_config, path, self._ENCODING)
    
    def deconfigure(self, device):
        path = os.path.join(self._tftpboot_dir, self._dev_specific_filename(device))
        try:
            os.remove(path)
        except OSError, e:
            # ignore
            logger.info('error while removing file: %s', e)
    
    def synchronize(self, device, raw_config):
        device_name = 'SEP' + format_mac(device[u'mac'], separator='', uppercase=True).encode('ascii')
        sync_service = synchronize.get_sync_service()
        if sync_service is None or sync_service.TYPE != 'AsteriskAMI':
            return defer.fail(Exception('Incompatible sync service: %s' % sync_service))
        else:
            return threads.deferToThread(sync_service.sccp_reset, device_name)
