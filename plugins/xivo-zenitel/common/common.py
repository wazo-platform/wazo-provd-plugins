# -*- coding: utf-8 -*-

# Copyright (C) 2011-2014 Avencall
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

"""Common code shared by the the various xivo-zenitel plugins.

"""


import logging
import re
import os.path
import urllib2
from operator import itemgetter
from provd.devices.config import RawConfigError
from provd.devices.pgasso import IMPROBABLE_SUPPORT, COMPLETE_SUPPORT, UNKNOWN_SUPPORT,\
    BasePgAssociator
from provd.plugins import StandardPlugin, TemplatePluginHelper,\
    FetchfwPluginHelper
from provd.servers.tftp.service import TFTPFileService
from provd.services import JsonConfigPersister,\
    PersistentConfigureServiceDecorator
from provd.util import norm_mac, format_mac
from twisted.internet import defer, threads

logger = logging.getLogger('plugin.xivo-zenitel')


class BaseZenitelTFTPDeviceInfoExtractor(object):
    _FILENAME_REGEX = re.compile(r'^ipst_config((?:_\w\w){6})?\.cfg$')
    
    def extract(self, request, request_type):
        return defer.succeed(self._do_extract(request))
    
    def _do_extract(self, request):
        # filename:
        #   "ipst_config.cfg"
        #   "ipst_config_01_02_03_04_05_ab.cfg"
        filename = request['packet']['filename']
        m = self._FILENAME_REGEX.match(filename)
        if m:
            dev_info = {u'vendor': u'Zenitel',
                        u'model': u'IP station'}
            raw_mac = m.group(1)
            if raw_mac:
                raw_mac = raw_mac.replace('_', '')
                try:
                    dev_info[u'mac'] = norm_mac(raw_mac.decode('ascii'))
                except ValueError, e:
                    logger.warning('Could not normalize MAC address: %s', e)
            return dev_info
        return None


class BaseZenitelPgAssociator(BasePgAssociator):
    def _do_associate(self, vendor, model, version):
        if vendor == u'Zenitel':
            if model == u'IP station':
                return COMPLETE_SUPPORT
            else:
                return UNKNOWN_SUPPORT
        else:
            return IMPROBABLE_SUPPORT


class ZenitelConfigureService(object):
    _URI = 'https://alphasupport.zenitel.com/alphawiki/'
    
    def __init__(self, auth_downloader, username, password):
        # username and password can be None
        self._auth_downloader = auth_downloader
        self._p_username = username
        self._p_password = password
        self._update_dler()
    
    def _update_dler(self):
        if self._p_username and self._p_password:
            self._auth_downloader.add_password(None, self._URI,
                                               self._p_username,
                                               self._p_password)
        else:
            # XXX this use some knowledge of the underlying implementation:
            # * AuthDownloader.add_password is just a wrapper around
            #   urllib2.HTTPPasswordManager.add_password
            # * urllib2.HTTPPaswordManager accept (None, None) as username
            #   and password
            self._auth_downloader.add_password(None, self._URI,
                                               None, None)
    
    def get(self, name):
        try:
            return getattr(self, '_p_' + name)
        except AttributeError, e:
            raise KeyError(e)
    
    def set(self, name, value):
        attrname = '_p_' + name
        if hasattr(self, attrname):
            setattr(self, attrname, value)
            self._update_dler()
        else:
            raise KeyError(name)
    
    description = [
        (u'username', u'The username used to download files on the alphawiki'),
        (u'password', u'The password used to download files on the alphawiki'),
    ]
    
    description_fr = [
        (u'username', u"Le nom d'utilisateur pour télécharger les fichiers sur le alphawiki"),
        (u'password', u'Le mot de passe pour télécharger les fichiers sur le alphawiki'),
    ]


class BaseZenitelPlugin(StandardPlugin):
    _ENCODING = 'UTF-8'
    _VALID_FUNCKEY_NO = [u'1', u'2', u'3']
    
    def __init__(self, app, plugin_dir, gen_cfg, spec_cfg):
        StandardPlugin.__init__(self, app, plugin_dir, gen_cfg, spec_cfg)
        
        self._tpl_helper = TemplatePluginHelper(plugin_dir)
        
        downloaders = FetchfwPluginHelper.new_downloaders(gen_cfg.get('proxies'))
        fetchfw_helper = FetchfwPluginHelper(plugin_dir, downloaders)
        
        cfg_service = ZenitelConfigureService(downloaders['auth'],
                                              spec_cfg.get('username'),
                                              spec_cfg.get('password'))
        persister = JsonConfigPersister(os.path.join(self._plugin_dir, 'var',
                                                     'config.json'))
        cfg_service = PersistentConfigureServiceDecorator(cfg_service, persister)
        
        self.services = {'configure': cfg_service,
                         'install': fetchfw_helper}
        self.tftp_service = TFTPFileService(self._tftpboot_dir)

    tftp_dev_info_extractor = BaseZenitelTFTPDeviceInfoExtractor()
    
    pg_associator = BaseZenitelPgAssociator()
    
    def _add_sip_section_info(self, raw_config):
        if u'1' in raw_config[u'sip_lines']:
            line = raw_config[u'sip_lines'][u'1']
            raw_config[u'XX_sip'] = True
            raw_config[u'XX_nick_name'] = line[u'display_name']
            raw_config[u'XX_sip_id'] = line[u'username']
            raw_config[u'XX_domain'] = line.get(u'proxy_ip') or raw_config[u'sip_proxy_ip']
            raw_config[u'XX_domain2'] = line.get(u'backup_proxy_ip') or \
                                        raw_config.get(u'backup_proxy_ip', u'')
            raw_config[u'XX_auth_user'] = line[u'auth_username']
            raw_config[u'XX_auth_pwd'] = line[u'password']
    
    def _add_fkeys(self, raw_config):
        lines = []
        for funckey_no, funckey_dict in sorted(raw_config[u'funckeys'].iteritems(),
                                               key=itemgetter(0)):
            if funckey_no in self._VALID_FUNCKEY_NO:
                if funckey_dict[u'type'] == u'speeddial':
                    exten = funckey_dict[u'value']
                    lines.append(u'speeddial_%s_c1=%s' % (funckey_no, exten))
                else:
                    logger.info('Unsupported funckey type: %s', funckey_dict[u'type'])
            else:
                logger.info('Out of range funckey no: %s', funckey_no)
        raw_config[u'XX_fkeys'] = u'\n'.join(' ' + s for s in lines)
    
    def _dev_specific_filename(self, device):
        # Return the device specific filename (not pathname) of device
        fmted_mac = format_mac(device[u'mac'], separator='_', uppercase=False)
        return 'ipst_config_%s.cfg' % fmted_mac
    
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
        
        self._add_sip_section_info(raw_config)
        self._add_fkeys(raw_config)
        
        path = os.path.join(self._tftpboot_dir, filename)
        self._tpl_helper.dump(tpl, raw_config, path, self._ENCODING)
    
    def deconfigure(self, device):
        path = os.path.join(self._tftpboot_dir, self._dev_specific_filename(device))
        try:
            os.remove(path)
        except OSError, e:
            # ignore
            logger.info('error while removing file: %s', e)
    
    def _do_synchronize(self, ip):
        # XXX could use twisted native http stuff one day...
        url = "http://%s/goform/zForm_send_cmd" % ip
        pwd_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
        pwd_manager.add_password(None, url, 'admin', 'alphaadmin')
        basic_auth_handler = urllib2.HTTPBasicAuthHandler(pwd_manager)
        opener = urllib2.build_opener(basic_auth_handler)
        fobj = opener.open(url, 'message=Reboot', 15)
        try:
            fobj.read()
        except Exception, e:
            logger.info('Exception during read from Zenitel synchronize: %s', e)
        finally:
            fobj.close()
    
    def synchronize(self, device, raw_config):
        try:
            ip = device[u'ip']
        except KeyError:
            return defer.fail(Exception('IP address needed for device synchronization'))
        else:
            return threads.deferToThread(self._do_synchronize, ip)
