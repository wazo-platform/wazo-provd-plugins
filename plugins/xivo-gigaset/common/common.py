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

"""Common code shared by the the various xivo-gigaset plugins.

"""


import cookielib
import logging
import re
import urllib
import urllib2
from ConfigParser import RawConfigParser
from contextlib import closing
from StringIO import StringIO
from provd.devices.pgasso import BasePgAssociator, IMPROBABLE_SUPPORT,\
    COMPLETE_SUPPORT, UNKNOWN_SUPPORT
from provd.plugins import StandardPlugin, TemplatePluginHelper
from provd.util import norm_mac
from twisted.internet import defer, threads

logger = logging.getLogger('plugin.xivo-gigaset')

VENDOR = u'Gigaset'


class BaseGigasetDHCPDeviceInfoExtractor(object):
    _VDI = {
        'C470IP':  u'C470 IP',
        'C470_IP': u'C470 IP',
        'S675IP':  u'S675 IP',
        'S675_IP': u'S675 IP',
        'C590_IP': u'C590 IP',
        'C610_IP': u'C610 IP'
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
        #   "C470IP"
        #   "C470_IP"
        #   "S675IP"
        #   "S675_IP"
        #   "C590_IP"
        if vdi in self._VDI:
            return {u'vendor': VENDOR,
                    u'model': self._VDI[vdi]}
        else:
            return None


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


class GigasetInteractionError(Exception):
    pass


class BaseGigasetRequestBroker(object):
    DEFAULT_PIN = '0000'
    DEFAULT_TIMEOUT = 15
    _MAC_REGEX = re.compile(r'\b[\dA-F]{2}(?::[\dA-F]{2}){5}\b')
    # _VERSION_REGEX should be present in (derived) instance of this class
    
    def __init__(self, host, pin=None):
        self._host = host
        self._pin = pin or self.DEFAULT_PIN
        self._url_prefix = 'http://%s/' % host
        self._cookie_jar = cookielib.CookieJar()
        self._opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self._cookie_jar))
    
    def login(self):
        raw_data = 'language=1&password=%s' % self._pin
        with self.do_post_request('login.html', raw_data) as fobj:
            fobj.read()
            url = fobj.geturl()
        
        if '/security_advice.html' in url:
            logger.debug('Logged succesfully with security advice to %s', self._host)
            raw_data = 'disable_advice=0'
            with self.do_post_request('security_advice.html', raw_data) as fobj:
                fobj.read()
        elif '/home.html' in url:
            logger.debug('Logged succesfully to %s', self._host)
        else:
            logger.warning('Failed login to %s', self._host)
            raise GigasetInteractionError('login failed')
    
    def logout(self):
        with self.do_get_request('logout.html') as fobj:
            fobj.read()
        self._cookie_jar.clear()
    
    def _do_request(self, url, data=None):
        logger.info('Making %s request to %s', 'POST' if data else 'GET', url)
        return closing(self._opener.open(url, data, timeout=self.DEFAULT_TIMEOUT))
    
    def _compute_url(self, path):
        # Note that path MUST NOT contain a leading slash, i.e. it must be
        # "login.html", not "/login.html"
        return self._url_prefix + path
    
    def do_get_request(self, path):
        return self._do_request(self._compute_url(path))
    
    def do_post_request(self, path, raw_data):
        url = self._compute_url(path)
        if isinstance(raw_data, basestring):
            data = raw_data
        else:
            data = urllib.urlencode(raw_data)
        return self._do_request(url, data)
    
    def _is_valid_line_no(self, line_no):
        return line_no >= 1 and line_no <= 6
    
    def _check_is_valid_line_no(self, line_no):
        if not self._is_valid_line_no(line_no):
            raise ValueError('invalid line number: %s' % line_no)
    
    def set_line(self, line_no, **kwargs):
        self._check_is_valid_line_no(line_no)

        logger.debug('Setting line %s', line_no)
        id_no = line_no - 1
        path = 'settings_telephony_voip.html?id=%s' % id_no
        raw_data = {
            'go_profile': '0',
            'account_id': id_no,
            'sip_password': kwargs['password'],
            'do_delete': '0',
            'account_name': kwargs.get('account_name', 'IP%s' % line_no),
            'autocode': '',
            'sip_login_id': kwargs['auth_username'],
            'sip_password_2': kwargs['password'],
            'sip_user_id': kwargs['username'],
            'sip_display_name': kwargs['display_name'],
            'sip_domain': kwargs.get('domain') or kwargs['proxy_ip'],
            'sip_server': kwargs['proxy_ip'],
            'sip_server_port': kwargs.get('proxy_port', '5060'),
            'sip_registrar': kwargs['registrar_ip'],
            'sip_registrar_port': kwargs.get('registrar_port', '5060'),
            'reg_refresh_time': '3600',
            'stun_mode': '0',
            'stun_server': '',
            'stun_port': '3478',
            'stun_refresh_time': '240',
            'nat_refresh_time': '20',
            'outbound_mode': '1',
            'outbound_proxy': kwargs.get('outbound_proxy_ip', ''),
            'outbound_port': '5060',
        }
        with self.do_post_request(path, raw_data) as fobj:
            fobj.read()
    
    def delete_line(self, line_no):
        self._check_is_valid_line_no(line_no)
        
        logger.debug('Deleting line %s', line_no)
        id_no = line_no - 1
        path = 'settings_telephony_voip.html?id=%s' % id_no
        raw_data = 'account_id=%s&do_delete=1' % id_no
        with self.do_post_request(path, raw_data) as fobj:
            fobj.read()
    
    def disable_gigasetnet_line(self):
        # should be implemented in derived classes
        logger.warning('Method not implemented: disable_gigasetnet_line')
    
    def set_mailboxes(self, dict_):
        # should be implemented in derived classes
        logger.warning('Method not implemented: set_mailboxes')
    
    def get_device_info(self):
        with self.do_get_request('status_device.html') as fobj:
            content = fobj.read()
        
        dev_info = {u'vendor': VENDOR}
        
        cur_pos = content.find('MAC address:')
        if cur_pos == -1:
            logger.warning('could not find "MAC address:" string')
            return
        m = self._MAC_REGEX.search(content, cur_pos)
        if not m:
            logger.warning('could not find MAC address')
            return
        raw_mac = m.group()
        cur_pos = m.end()
        dev_info[u'mac'] = norm_mac(raw_mac.decode('ascii'))
        
        if hasattr(self, '_VERSION_REGEX'):
            cur_pos = content.find('Firmware version:', cur_pos)
            if cur_pos == -1:
                logger.warning('could not find "Firmware version:" string')
                return
            m = self._VERSION_REGEX.search(content, cur_pos)
            if not m:
                logger.warning('could not find firmware version')
                return
            raw_version = m.group(1)
            dev_info[u'version'] = raw_version.decode('ascii')
        
        return dev_info


class BaseGigasetPlugin(StandardPlugin):
    _ENCODING = 'UTF-8'
    # _BROKER_FACTORY attribute must be present in (derived) instance of this class
    
    def __init__(self, app, plugin_dir, gen_cfg, spec_cfg):
        StandardPlugin.__init__(self, app, plugin_dir, gen_cfg, spec_cfg)
        self._app = app
        
        self._tpl_helper = TemplatePluginHelper(plugin_dir)
        
    dhcp_dev_info_extractor = BaseGigasetDHCPDeviceInfoExtractor()
    
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
        # 1. generate template and read it as our own config for our broker
        tpl = self._tpl_helper.get_dev_template(raw_config.get(u'mac'), device)
        fobj = StringIO(tpl.render(raw_config))
        
        config = RawConfigParser()
        config.readfp(fobj)
        fobj.close()
        
        general = dict(config.items('general'))
        
        # 2. instantiate broker and do requests...
        host = device[u'ip']
        pin = general.get('pin')
        broker = self._BROKER_FACTORY(host, pin)
        
        broker.login()
        try:
            # update info
            if general.get('skip_update_infos') != '1':
                dev_info = broker.get_device_info()
                if dev_info:
                    device.update(dev_info)
                    from twisted.internet import reactor
                    reactor.callFromThread(self._app.dev_update, device)
            
            # configure lines
            if general.get('skip_lines_configuration') != '1':
                for line_no in xrange(1, 7):
                    line_no_str = str(line_no)
                    if line_no_str in raw_config[u'sip_lines']:
                        line = raw_config[u'sip_lines'][line_no_str]
                        kwargs = {
                            'password': line[u'password'],
                            'auth_username': line[u'auth_username'],
                            'username': line[u'username'],
                            'display_name': line[u'display_name'],
                            'proxy_ip': line.get(u'proxy_ip') or \
                                        raw_config[u'sip_proxy_ip'],
                            'proxy_port': line.get(u'proxy_port') or \
                                          raw_config.get(u'proxy_port', '5060'),
                            'registrar_ip': line.get(u'registrar_ip') or \
                                            raw_config[u'sip_registrar_ip'],
                            'registrar_port': line.get(u'registrar_port') or \
                                              raw_config.get(u'registrar_port', '5060')
                        }
                        broker.set_line(line_no, **kwargs)
                    else:
                        if general.get('skip_delete_line') != '1':
                            broker.delete_line(line_no)
            
            # disable gigaset line
            if general.get('skip_disable_gigasetnet_line') != '1':
                broker.disable_gigasetnet_line()
            
            # configure mailboxes
            if general.get('skip_mailboxes_configuration') != '1':
                mailboxes = {}
                for line_no_str, line in raw_config[u'sip_lines'].iteritems():
                    line_no = int(line_no_str)
                    voicemail = line.get(u'voicemail') or raw_config.get(u'exten_voicemail')
                    if voicemail:
                        mailboxes[line_no] = voicemail 
            
            # do generic requests stuff here
            config_dict = dict((s, dict(config.items(s))) for s in config.sections() if s != 'general')
            for path, raw_data in config_dict.iteritems():
                with broker.do_post_request(path, raw_data) as fobj:
                    fobj.read()
        finally:
            broker.logout()
    
    def synchronize(self, device, raw_config):
        assert u'ip' in device      # see self.configure() and plugin contract
        
        return threads.deferToThread(self._do_synchronize, device, raw_config)
