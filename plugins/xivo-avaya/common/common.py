# -*- coding: utf-8 -*-

# Copyright 2011-2019 The Wazo Authors  (see the AUTHORS file)
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

"""Common code shared by the the various xivo-avaya plugins.

Support the 1220IP and 1230IP.

"""


import re
import os
import logging
from provd import tzinform
from provd import synchronize
from provd.devices.config import RawConfigError
from provd.devices.pgasso import BasePgAssociator, FULL_SUPPORT,\
    COMPLETE_SUPPORT, PROBABLE_SUPPORT, IMPROBABLE_SUPPORT
from provd.plugins import StandardPlugin, TemplatePluginHelper,\
    FetchfwPluginHelper
from provd.servers.http import HTTPNoListingFileService
from provd.servers.tftp.service import TFTPFileService
from provd.util import format_mac, norm_mac
from twisted.internet import defer, threads

logger = logging.getLogger('plugin.xivo-avaya')


_FILENAME_MAP = {
    '1220.cfg': u'1220IP',
    '1220SIP.cfg': u'1220IP',
    '1230.cfg': u'1230IP',
    '1230SIP.cfg': u'1230IP',
}

class BaseAvayaHTTPDeviceInfoExtractor(object):
    _UA_REGEX = re.compile(r'^AVAYA/[^/]+/([\d.]{11})$')
    _PATH_REGEX = re.compile(r'\bSIP([\dA-F]{12})\.cfg$')
    
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
        #   "AVAYA/SIP12x0\x17/04.00.04.00"
        #   "AVAYA/SIP12x0\x16/04.00.04.00"
        #   "AVAYA/SIP12x0\x14/04.00.04.00"
        #   "AVAYA/SIP12x0\xff/04.01.13.00"
        m = self._UA_REGEX.match(ua)
        if m:
            raw_version = m.group(1)
            return {u'vendor': u'Avaya',
                    u'version': raw_version.decode('ascii')}
        return None
    
    def _extract_from_path(self, path, dev_info):
        m = self._PATH_REGEX.search(path)
        if m:
            raw_mac = m.group(1)
            dev_info[u'mac'] = norm_mac(raw_mac.decode('ascii'))
        else:
            filename = os.path.basename(path)
            if filename in _FILENAME_MAP:
                dev_info[u'model'] = _FILENAME_MAP[filename]


class BaseAvayaTFTPDeviceInfoExtractor(object):
    # TFTP is only used for the update from UNIStim to SIP, so we only
    # need minimal information to get the plugin association working.
    
    def extract(self, request, request_type):
        return defer.succeed(self._do_extract(request))
    
    def _do_extract(self, request):
        filename = request['packet']['filename']
        if filename in _FILENAME_MAP:
            return {u'vendor': u'Avaya', u'model': _FILENAME_MAP[filename]}
        return None


class BaseAvayaPgAssociator(BasePgAssociator):
    def __init__(self, models, version):
        BasePgAssociator.__init__(self)
        self._models = models
        self._version = version
    
    def _do_associate(self, vendor, model, version):
        if vendor == u'Avaya':
            if model in self._models:
                if version == self._version:
                    return FULL_SUPPORT
                # XXX if there's one day a plugin supporting UNIStim (...),
                #     then we might want to do more check on the version,
                #     or return a lower support value
                return COMPLETE_SUPPORT
            return PROBABLE_SUPPORT
        return IMPROBABLE_SUPPORT


class BaseAvayaPlugin(StandardPlugin):
    # XXX file encoding is not stated anywhere
    _ENCODING = 'UTF-8'
    
    def __init__(self, app, plugin_dir, gen_cfg, spec_cfg):
        StandardPlugin.__init__(self, app, plugin_dir, gen_cfg, spec_cfg)
        
        self._tpl_helper = TemplatePluginHelper(plugin_dir)
        
        downloaders = FetchfwPluginHelper.new_downloaders(gen_cfg.get('proxies'))
        fetchfw_helper = FetchfwPluginHelper(plugin_dir, downloaders)
        
        self.services = fetchfw_helper.services()
        self.tftp_service = TFTPFileService(self._tftpboot_dir)
        self.http_service = HTTPNoListingFileService(self._tftpboot_dir)
    
    http_dev_info_extractor = BaseAvayaHTTPDeviceInfoExtractor()
    
    tftp_dev_info_extractor = BaseAvayaTFTPDeviceInfoExtractor()
    
    def _add_timezone(self, raw_config):
        if u'timezone' in raw_config:
            try:
                tzinfo = tzinform.get_timezone_info(raw_config[u'timezone'])
            except tzinform.TimezoneNotFoundError, e:
                logger.warning('Unknown timezone: %s', e)
            else:
                raw_config[u'XX_timezone'] = u'TIMEZONE_OFFSET %d' % tzinfo['utcoffset'].as_seconds
    
    def _dev_specific_filename(self, device):
        # Return the device specific filename (not pathname) of device
        fmted_mac = format_mac(device[u'mac'], separator='', uppercase=True)
        return 'SIP%s.cfg' % fmted_mac
    
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
        
        self._add_timezone(raw_config)
        
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
