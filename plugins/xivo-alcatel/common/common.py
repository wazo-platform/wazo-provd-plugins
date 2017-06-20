# -*- coding: utf-8 -*-

# Copyright (C) 2011-2016 Avencall
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

"""Common code shared by the various xivo-alcatel plugins.

Support the IP Touch 4008EE and 4018EE.

"""



import calendar
import datetime
import logging
import os.path
import re
import time
from provd import tzinform
from provd.devices.config import RawConfigError
from provd.plugins import StandardPlugin, FetchfwPluginHelper,\
    TemplatePluginHelper
from provd.devices.pgasso import IMPROBABLE_SUPPORT, PROBABLE_SUPPORT,\
    COMPLETE_SUPPORT, FULL_SUPPORT, BasePgAssociator
from provd.servers.http import HTTPNoListingFileService
from provd.servers.tftp.service import TFTPFileService
from provd.util import norm_mac, format_mac
from twisted.internet import defer, threads

logger = logging.getLogger('plugin.xivo-alcatel')

VENDOR = u'Alcatel'


class BaseAlcatelHTTPDeviceInfoExtractor(object):
    _UA_REGEX = re.compile(r'^Alcatel IP Touch (\d+)/([\w.]+)$')
    _PATH_REGEX = re.compile(r'\bsipconfig-(\w+)\.txt$')
    
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
        # Note that the MAC address if not present in User-Agent and so will
        # never be returned by this function.
        # HTTP User-Agent:
        #   "Alcatel IP Touch 4008/2.00.81"
        #   "Alcatel IP Touch 4008/2.01.10"
        #   "Alcatel IP Touch 4018/2.01.10"
        m = self._UA_REGEX.match(ua)
        if m:
            raw_model, raw_version = m.groups()
            return {u'vendor': VENDOR,
                    u'model': raw_model.decode('ascii'),
                    u'version': raw_version.decode('ascii')}
        return None
    
    def _extract_from_path(self, path, dev_info):
        # try to extract MAC address from path
        m = self._PATH_REGEX.search(path)
        if m:
            raw_mac = m.group(1)
            try:
                mac = norm_mac(raw_mac.decode('ascii'))
            except ValueError, e:
                logger.warning('Could not normalize MAC address: %s', e)
            else:
                dev_info[u'mac'] = mac


class BaseAlcatelTFTPDeviceInfoExtractor(object):
    # We need a TFTP device extractor if we want to be able to update a phone
    # in NOE mode to SIP mode, since it seems like it's not possible for the
    # phone to do HTTP request in NOE mode
    
    def extract(self, request, request_type):
        return defer.succeed(self._do_extract(request))
    
    def _do_extract(self, request):
        filename = request['packet']['filename']
        if filename == '/lanpbx.cfg':
            return {u'vendor': VENDOR}
        return None


class BaseAlcatelPgAssociator(BasePgAssociator):
    def __init__(self, models, version):
        self._models = models
        self._version = version
    
    def _do_associate(self, vendor, model, version):
        if vendor == VENDOR:
            if model in self._models:
                if version == self._version:
                    return FULL_SUPPORT
                return COMPLETE_SUPPORT
            return PROBABLE_SUPPORT
        return IMPROBABLE_SUPPORT


class BaseAlcatelPlugin(StandardPlugin):
    _ENCODING = 'UTF-8'
    _DEFAULT_PASSWORD = u'000000'
    _SIP_TRANSPORT = {
        u'udp': u'1',
        u'tcp': u'2'
    }
    _SIP_DTMF_MODE = {
        u'RTP-in-band': u'1',
        u'RTP-out-of-band': u'0',
        u'SIP-INFO': u'2'
    }
    # XXX this is confused, but I don't care that much right now
    _TONE_COUNTRY = [
        # "English" tone country
        [u'US', u'CA'],
        # "French" tone country
        [u'FR'],
        # "German" tone country
        [u'DE'],
        # "Italian" tone country
        [u'IT'],
        # "Spanish" tone country
        [u'ES'],
        # "Dutch" tone country
        [],
        # "Portuguese" tone country
        []
    ]
    
    def __init__(self, app, plugin_dir, gen_cfg, spec_cfg):
        StandardPlugin.__init__(self, app, plugin_dir, gen_cfg, spec_cfg)
        
        self._tpl_helper = TemplatePluginHelper(plugin_dir)
        
        downloaders = FetchfwPluginHelper.new_downloaders(gen_cfg.get('proxies'))
        fetchfw_helper = FetchfwPluginHelper(plugin_dir, downloaders)
        
        self.services = fetchfw_helper.services()
        self.http_service = HTTPNoListingFileService(self._tftpboot_dir)
        self.tftp_service = TFTPFileService(self._tftpboot_dir)
    
    http_dev_info_extractor = BaseAlcatelHTTPDeviceInfoExtractor()
    
    tftp_dev_info_extractor = BaseAlcatelTFTPDeviceInfoExtractor()
    
    def _extract_sip_line_info(self, raw_config):
        assert raw_config[u'sip_lines']
        sip_lines_key = min(raw_config[u'sip_lines'])
        sip_line = raw_config[u'sip_lines'][sip_lines_key]
        def set_if(line_id, id):
            if line_id in sip_line:
                raw_config[id] = sip_line[line_id]
        set_if(u'proxy_ip', u'sip_proxy_ip')
        set_if(u'proxy_port', u'sip_proxy_port')
        set_if(u'backup_proxy_ip', u'sip_backup_proxy_ip')
        set_if(u'backup_proxy_port', u'sip_backup_proxy_port')
        set_if(u'outbound_proxy_ip', u'sip_outbound_proxy_ip')
        set_if(u'outbound_proxy_port', u'sip_outbound_proxy_port')
        set_if(u'registrar_ip', u'sip_registrar_ip')
        set_if(u'registrar_port', u'sip_registrar_port')
        set_if(u'backup_registrar_ip', u'sip_backup_registrar_ip')
        set_if(u'backup_registrar_port', u'sip_backup_registrar_port')
        
        raw_config[u'XX_auth_name'] = sip_line[u'auth_username']
        raw_config[u'XX_auth_password'] = sip_line[u'password']
        raw_config[u'XX_user_name'] = sip_line[u'username']
        raw_config[u'XX_display_name'] = sip_line[u'display_name']
        
        voicemail = sip_line.get(u'voicemail') or raw_config.get(u'exten_voicemail')
        if voicemail:
            raw_config[u'XX_voice_mail_uri'] = voicemail
            # XXX should we consider the value of sip_subscribe_mwi before ?
            raw_config[u'XX_mwi_uri'] = "%s@%s" % (voicemail, raw_config[u'sip_proxy_ip'])
    
    def _add_dns_addr(self, raw_config):
        # this function must be called after _extract_sip_line_info
        if raw_config.get(u'dns_enabled'):
            dns_addr = raw_config[u'dns_ip']
        else:
            dns_addr = raw_config[u'sip_proxy_ip']
        raw_config[u'XX_dns_addr'] = dns_addr
    
    def _add_sip_transport_mode(self, raw_config):
        try:
            sip_transport = self._SIP_TRANSPORT[raw_config[u'sip_transport']]
        except KeyError:
            logger.info('Unknown/unsupported sip_transport: %s',
                        raw_config[u'sip_transport'])
        else:
            raw_config[u'XX_sip_transport_mode'] = sip_transport
    
    def _add_sntp_addr(self, raw_config):
        if raw_config.get(u'ntp_enabled'):
            raw_config[u'XX_sntp_addr'] = raw_config[u'ntp_ip']
    
    def _format_dst_change(self, dst):
        if dst['day'].startswith('D'):
            day = int(dst['day'][1:])
        else:
            # compute the day of the month for the current year
            raw_week, raw_weekday = dst['day'][1:].split('.')
            week =  int(raw_week) - 1
            weekday = tzinform.week_start_on_monday(int(raw_weekday)) - 1
            current_year = datetime.datetime.utcnow().year
            month_calendar = calendar.monthcalendar(current_year, dst['month'])
            day = month_calendar[week][weekday]
        return '%02d%02d%02d' % (dst['month'], day, dst['time'].as_hours)
    
    def _format_tzinfo(self, tzinfo):
        offset = tzinfo['utcoffset'].as_minutes
        if tzinfo['dst']:
            dst_start = self._format_dst_change(tzinfo['dst']['start'])
            dst_end = self._format_dst_change(tzinfo['dst']['end'])
        else:
            dst_start = '000000'
            dst_end = '000000'
        return 'UT::%s:%s:%s' % (offset, dst_start, dst_end)
    
    def _add_timezone(self, raw_config):
        if u'timezone' in raw_config:
            try:
                tzinfo = tzinform.get_timezone_info(raw_config[u'timezone'])
            except tzinform.TimezoneNotFoundError, e:
                logger.info('Unknown timezone: %s', e)
            else:
                try:
                    raw_config[u'XX_timezone'] = self._format_tzinfo(tzinfo)
                except Exception:
                    logger.error('Error while formating tzinfo', exc_info=True)
    
    def _add_tone_country(self, raw_config):
        if u'locale' in raw_config:
            try:
                country = raw_config[u'locale'].rsplit('_', 1)[1]
            except IndexError:
                # locale is not of the form 'xx_XX'
                pass
            else:
                for i, countries in enumerate(self._TONE_COUNTRY):
                    if country in countries:
                        raw_config[u'XX_tone_country'] = unicode(i)
                        break
    
    def _add_dtmf_type(self, raw_config):
        if u'sip_dtmf_mode' in raw_config:
            try:
                dtmf_type = self._SIP_DTMF_MODE[raw_config[u'sip_dtmf_mode']]
            except KeyError:
                logger.info('Unknown/unsupported sip_dtmf_mode: %s',
                            raw_config[u'sip_dtmf_mode'])
            else:
                raw_config[u'XX_dtmf_type'] = dtmf_type
    
    def _add_fkeys(self, raw_config):
        lines = []
        for funckey_no, funckey_dict in raw_config[u'funckeys'].iteritems():
            int_funckey_no = int(funckey_no)
            if int_funckey_no > 4:
                logger.warning('Out of range funckey number: %s', funckey_no)
            else:
                funckey_type = funckey_dict[u'type']
                if funckey_type == u'speeddial':
                    value = funckey_dict[u'value']
                    # need to set a non-empty label for the funckey to works
                    label = funckey_dict.get(u'label', value)
                    lines.append('speed_dial_%s_first_name=%s' % (funckey_no, label))
                    lines.append('speed_dial_%s_uri=%s' % (funckey_no, value))
                else:
                    logger.warning('Unsupported funckey type: %s', funckey_type)
        raw_config[u'XX_fkeys'] = u'\n'.join(lines)
    
    def _update_admin_password(self, raw_config):
        raw_config.setdefault(u'admin_password', self._DEFAULT_PASSWORD)
    
    def _dev_specific_filename(self, device):
        # Return the device specific filename (not pathname) of device
        fmted_mac = format_mac(device[u'mac'], separator='', uppercase=False)
        return 'sipconfig-%s.txt' % fmted_mac
    
    def _check_config(self, raw_config):
        if u'http_port' not in raw_config:
            raise RawConfigError('only support configuration via HTTP')
        if not raw_config[u'sip_lines']:
            # the phone won't be configured properly if a sip line is not defined
            raise RawConfigError('need at least one sip lines defined')
    
    def _check_device(self, device):
        if u'mac' not in device:
            raise Exception('MAC address needed for device configuration')
    
    def configure(self, device, raw_config):
        self._check_config(raw_config)
        self._check_device(device)
        filename = self._dev_specific_filename(device)
        tpl = self._tpl_helper.get_dev_template(filename, device)
        
        self._extract_sip_line_info(raw_config)
        self._add_dns_addr(raw_config)
        self._add_sip_transport_mode(raw_config)
        self._add_sntp_addr(raw_config)
        self._add_timezone(raw_config)
        self._add_tone_country(raw_config)
        self._add_dtmf_type(raw_config)
        self._add_fkeys(raw_config)
        self._update_admin_password(raw_config)
        
        path = os.path.join(self._tftpboot_dir, filename)
        self._tpl_helper.dump(tpl, raw_config, path, self._ENCODING)
    
    def deconfigure(self, device):
        path = os.path.join(self._tftpboot_dir, self._dev_specific_filename(device))
        try:
            os.remove(path)
        except OSError, e:
            # ignore
            logger.info('error while removing file: %s', e)
    
    def _do_synchronize_via_telnet(self, ip, password):
        import pexpect
        child = pexpect.spawn('telnet', [ip], timeout=5)
        try:
            child.expect('Password ?')
            child.sendline(password)
            child.expect('Login accepted')
            child.sendline('reset soft')
            # wait a small time before closing the connection
            time.sleep(10)
        finally:
            child.close(force=True)
    
    def synchronize(self, device, raw_config):
        try:
            ip = device[u'ip'].encode('ascii')
        except KeyError:
            return defer.fail(Exception('IP address needed for device synchronization'))
        else:
            password = raw_config.get(u'admin_password', self._DEFAULT_PASSWORD).encode('ascii')
            return threads.deferToThread(self._do_synchronize_via_telnet, ip, password)

    def get_remote_state_trigger_filename(self, device):
        if u'mac' not in device:
            return None

        return self._dev_specific_filename(device)
