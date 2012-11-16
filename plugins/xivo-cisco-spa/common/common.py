# -*- coding: UTF-8 -*-

"""Common plugin code shared by the the various xivo-cisco-spa plugins.

"""

__license__ = """
    Copyright (C) 2010-2011  Avencall

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import errno
import logging
import os
import re
import subprocess
from binascii import b2a_hex
from operator import itemgetter
from xml.sax.saxutils import escape
from provd import tzinform
from provd import synchronize
from provd.devices.config import RawConfigError
from provd.devices.pgasso import BasePgAssociator, IMPROBABLE_SUPPORT, \
    PROBABLE_SUPPORT, COMPLETE_SUPPORT, FULL_SUPPORT
from provd.plugins import StandardPlugin, FetchfwPluginHelper, \
    TemplatePluginHelper
from provd.servers.http import HTTPNoListingFileService, HTTPHookService
from provd.servers.tftp.service import TFTPFileService
from provd.util import norm_mac, format_mac
from twisted.internet import defer, threads

logger = logging.getLogger('plugins.xivo-cisco-spa')


def _norm_model(raw_model):
    # Normalize a model name and return it as a unicode string. This removes
    # minus sign and make all the characters uppercase.
    return raw_model.replace('-', '').upper().decode('ascii')


class BaseCiscoDHCPDeviceInfoExtractor(object):
    _RAW_VENDORS = ['LINKSYS', 'Cisco']

    def extract(self, request, request_type):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request):
        options = request[u'options']
        if 60 in options:
            return self._extract_from_vdi(options[60])
        return None

    def _extract_from_vdi(self, vdi):
        # Vendor class identifier:
        #   "LINKSYS SPA-942" (SPA942 6.1.5a)
        #   "LINKSYS SPA-962" (SPA962 6.1.5a)
        #   "LINKSYS SPA8000" (SPA8000 unknown version)
        #   "Cisco SPA501G" (SPA501G 7.4.4)
        #   "Cisco SPA508G" (SPA508G 7.4.4)
        #   "Cisco SPA525g" (SPA525G unknown version, from Cisco documentation)
        #   "Cisco SPA525G" (SPA525G 7.4.4)
        #   "Cisco SPA525G" (SPA525G 7.4.7)
        #   "Cisco SPA525G2" (SPA525G2 7.4.5)
        tokens = vdi.split()
        if len(tokens) == 2:
            raw_vendor, raw_model = tokens
            if raw_vendor in self._RAW_VENDORS:
                dev_info = {u'vendor': u'Cisco',
                            u'model': _norm_model(raw_model)}
                return dev_info
        return None


class BaseCiscoHTTPDeviceInfoExtractor(object):
    _LINKSYS_UA_REGEX = re.compile(r'^Linksys/([\w\-]+)-([^\s\-]+) \((\w+)\)$')
    _CISCO_UA_REGEX = re.compile(r'^Cisco/(\w+)-(\S+) (?:\(([\dA-F]{12})\))?\((\w+)\)$')
    _PATH_REGEX = re.compile(r'\b([\da-f]{12})\.xml$')

    def extract(self, request, request_type):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request):
        ua = request.getHeader('User-Agent')
        if ua:
            dev_info = {}
            self._extract_from_ua(ua, dev_info)
            if dev_info:
                dev_info[u'vendor'] = u'Cisco'
                if u'mac' not in dev_info:
                    self._extract_from_path(request.path, dev_info)
                return dev_info
        return None

    def _extract_from_ua(self, ua, dev_info):
        # HTTP User-Agent:
        # Note: the last group of digit is the serial number;
        #       the first, if present, is the MAC address
        #   "Linksys/SPA-942-6.1.5(a) (88019FA42805)"
        #   "Linksys/SPA-962-6.1.5(a) (4MM00F903042)"
        #   "Cisco/SPA501G-7.4.4 (8843E157DDCC)(CBT141100HR)"
        #   "Cisco/SPA508G-7.4.4 (0002FDFF2103)(CBT141400UK)"
        #   "Cisco/SPA508G-7.4.8a (0002FDFF2103)(CBT141400UK)"
        #   "Cisco/SPA525G-7.4.4 (CBT141900G7)"
        #   "Cisco/SPA525G-7.4.7 (CBT141900G7)"
        if ua.startswith('Linksys/'):
            self._extract_linksys_from_ua(ua, dev_info)
        elif ua.startswith('Cisco/'):
            self._extract_cisco_from_ua(ua, dev_info)

    def _extract_linksys_from_ua(self, ua, dev_info):
        # Pre: ua.startswith('Linksys/')
        m = self._LINKSYS_UA_REGEX.match(ua)
        if m:
            raw_model, version, sn = m.groups()
            dev_info[u'model'] = _norm_model(raw_model)
            dev_info[u'version'] = version.decode('ascii')
            dev_info[u'sn'] = sn.decode('ascii')

    def _extract_cisco_from_ua(self, ua, dev_info):
        # Pre: ua.startswith('Cisco/')
        m = self._CISCO_UA_REGEX.match(ua)
        if m:
            model, version, raw_mac, sn = m.groups()
            dev_info[u'model'] = model.decode('ascii')
            dev_info[u'version'] = version.decode('ascii')
            if raw_mac:
                dev_info[u'mac'] = norm_mac(raw_mac.decode('ascii'))
            dev_info[u'sn'] = sn.decode('ascii')

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


class BaseCiscoTFTPDeviceInfoExtractor(object):
    _SEPFILE_REGEX = re.compile(r'^SEP([\dA-F]{12})\.cnf\.xml$')
    _SPAFILE_REGEX = re.compile(r'^/spa(.+?)\.cfg$')

    def extract(self, request, request_type):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request):
        packet = request['packet']
        filename = packet['filename']
        for test_fun in [self._test_sepfile, self._test_spafile, self._test_init]:
            dev_info = test_fun(filename)
            if dev_info:
                dev_info[u'vendor'] = u'Cisco'
                return dev_info
        return None

    def _test_sepfile(self, filename):
        # Test if filename is "SEPMAC.cnf.xml".
        m = self._SEPFILE_REGEX.match(filename)
        if m:
            raw_mac = m.group(1)
            return {u'mac': norm_mac(raw_mac.decode('ascii'))}
        return None

    def _test_spafile(self, filename):
        # Test if filename is "/spa$PSN.cfg".
        m = self._SPAFILE_REGEX.match(filename)
        if m:
            raw_model = 'SPA' + m.group(1)
            return {u'model': _norm_model(raw_model)}
        return None

    def _test_init(self, filename):
        # Test if filename is "/init.cfg".
        if filename == '/init.cfg':
            return {u'model': u'PAP2T'}
        return None


class BaseCiscoPgAssociator(BasePgAssociator):
    def __init__(self, model_version):
        BasePgAssociator.__init__(self)
        self._model_version = model_version

    def _do_associate(self, vendor, model, version):
        if vendor == u'Cisco':
            if model in self._model_version:
                if version == self._model_version[model]:
                    return FULL_SUPPORT
                return COMPLETE_SUPPORT
            if model is not None:
                # model is unknown to the plugin, chance are low
                # that's it's going to be supported because of missing
                # common configuration file that are used to bootstrap
                # the provisioning process
                return IMPROBABLE_SUPPORT
            return PROBABLE_SUPPORT
        return IMPROBABLE_SUPPORT


class BaseCiscoHTTPHookService(HTTPHookService):
    # HTTP handler to support the config file encryption mess.

    def __init__(self, service, plugin):
        HTTPHookService.__init__(self, service)
        self._plugin = plugin

    def _pre_handle(self, path, request):
        # XXX we might also want to remove the encrypted file when
        #     it's no more needed, although there isn't any real problem
        #     about leaving it there
        if request.path.endswith('.xml.encrypted'):
            device = request.prov_dev
            if not device[u'X_xivo_cisco_spa_encrypted']:
                # remove the unencrypted configuration file
                filename = self._plugin._dev_specific_filename(device)
                path = os.path.join(self._plugin._tftpboot_dir, filename)
                logger.info('Removing unencrypted file %s', path)
                try:
                    os.remove(path)
                except OSError, e:
                    # probably an already removed file
                    logger.warning('Could not remove unencrypted file: %s', e)
                device[u'X_xivo_cisco_spa_encrypted'] = True
                self._plugin._app.dev_update(device)


class BaseCiscoPlugin(StandardPlugin):
    """Base classes MUST have a '_COMMON_FILENAMES' attribute which is a
    sequence of filenames that will be generated by the common template in
    the common_configure function.
    
    """

    _ENCODING = 'UTF-8'
    _NB_FKEY = {
        # <model>: (<nb keys>, <nb expansion modules>)
        u'SPA941': (4, 0),
        u'SPA942': (4, 0),
        u'SPA962': (6, 2),
        u'SPA303': (3, 2),
        u'SPA501G': (8, 2),
        u'SPA502G': (2, 2),
        u'SPA504G': (4, 2),
        u'SPA508G': (8, 2),
        u'SPA509G': (12, 2),
        u'SPA525G': (5, 2),
        u'SPA525G2': (5, 2)
    }
    _LOCALE = {
        u'de_DE': u'German',
        u'en_US': u'English',
        u'es_ES': u'Spanish',
        u'fr_FR': u'French',
        u'fr_CA': u'French',
    }

    def __init__(self, app, plugin_dir, gen_cfg, spec_cfg):
        StandardPlugin.__init__(self, app, plugin_dir, gen_cfg, spec_cfg)
        self._app = app
        self._cache_dir = os.path.join(plugin_dir, 'var', 'cache')

        self._tpl_helper = TemplatePluginHelper(plugin_dir)

        downloaders = FetchfwPluginHelper.new_downloaders(gen_cfg.get('proxies'))
        fetchfw_helper = FetchfwPluginHelper(plugin_dir, downloaders)

        self.services = fetchfw_helper.services()
        self.http_service = BaseCiscoHTTPHookService(HTTPNoListingFileService(self._tftpboot_dir), self)
        self.tftp_service = TFTPFileService(self._tftpboot_dir)

    dhcp_dev_info_extractor = BaseCiscoDHCPDeviceInfoExtractor()

    http_dev_info_extractor = BaseCiscoHTTPDeviceInfoExtractor()

    tftp_dev_info_extractor = BaseCiscoTFTPDeviceInfoExtractor()

    def configure_common(self, raw_config):
        tpl = self._tpl_helper.get_template('common/model.cfg.tpl')
        common_filenames = self._COMMON_FILENAMES
        for filename in common_filenames:
            dst = os.path.join(self._tftpboot_dir, filename)
            self._tpl_helper.dump(tpl, raw_config, dst, self._ENCODING)

    def _add_fkeys(self, raw_config, model):
        if model not in self._NB_FKEY:
            logger.info(u'Unknown model or model with no funckeys: %s', model)
            return
        nb_keys, nb_expmods = self._NB_FKEY[model]
        lines = []
        for funckey_no, funckey_dict in sorted(raw_config[u'funckeys'].iteritems(),
                                               key=itemgetter(0)):
            funckey_type = funckey_dict[u'type']
            if funckey_type == u'speeddial':
                fnc = u'sd+cp'
            elif funckey_type == u'blf':
                fnc = u'sd+cp+blf'
            else:
                logger.info('Unsupported funckey type: %s', funckey_type)
                continue
            value = funckey_dict[u'value']
            label = escape(funckey_dict.get(u'label', value))
            function = u'fnc=%s;sub=%s@$PROXY;nme=%s' % (fnc, value, label)
            keynum = int(funckey_no)
            if keynum <= nb_keys:
                lines.append(u'<Extension_%s_>Disabled</Extension_%s_>' %
                             (funckey_no, funckey_no))
                lines.append(u'<Short_Name_%s_>%s</Short_Name_%s_>' %
                             (funckey_no, label, funckey_no))
                lines.append(u'<Extended_Function_%s_>%s</Extended_Function_%s_>' %
                             (funckey_no, function, funckey_no))
            else:
                expmod_keynum = keynum - nb_keys - 1
                expmod_no = expmod_keynum // 32 + 1
                if expmod_no > nb_expmods:
                    logger.info('Model %s has less than %s function keys', model, funckey_no)
                else:
                    expmod_key_no = expmod_keynum % 32 + 1
                    lines.append(u'<Unit_%s_Key_%s>%s</Unit_%s_Key_%s>' %
                                 (expmod_no, expmod_key_no, function, expmod_no, expmod_key_no))
        raw_config[u'XX_fkeys'] = u'\n'.join(lines)

    def _format_dst_change(self, dst_change):
        _day = dst_change['day']
        if _day.startswith('D'):
            day = _day[1:]
            weekday = '0'
        else:
            week, weekday = _day[1:].split('.')
            weekday = tzinform.week_start_on_monday(int(weekday))
            if week == '5':
                day = '-1'
            else:
                day = (int(week) - 1) * 7 + 1

        h, m, s = dst_change['time'].as_hms
        return u'%s/%s/%s/%s:%s:%s' % (dst_change['month'], day, weekday, h, m, s)

    def _format_tzinfo(self, tzinfo):
        lines = []
        hours, minutes = tzinfo['utcoffset'].as_hms[:2]
        lines.append(u'<Time_Zone>GMT%+03d:%02d</Time_Zone>' % (hours, minutes))
        if tzinfo['dst'] is None:
            lines.append(u'<Daylight_Saving_Time_Enable>no</Daylight_Saving_Time_Enable>')
        else:
            lines.append(u'<Daylight_Saving_Time_Enable>yes</Daylight_Saving_Time_Enable>')
            h, m, s = tzinfo['dst']['save'].as_hms
            lines.append(u'<Daylight_Saving_Time_Rule>start=%s;end=%s;save=%d:%d:%s</Daylight_Saving_Time_Rule>' %
                         (self._format_dst_change(tzinfo['dst']['start']),
                          self._format_dst_change(tzinfo['dst']['end']),
                          h, m, s,
                          ))
        return u'\n'.join(lines)

    def _add_timezone(self, raw_config):
        if u'timezone' in raw_config:
            try:
                tzinfo = tzinform.get_timezone_info(raw_config[u'timezone'])
            except tzinform.TimezoneNotFoundError, e:
                logger.info('Unknown timezone: %s', e)
            else:
                raw_config[u'XX_timezone'] = self._format_tzinfo(tzinfo)

    def _format_proxy(self, raw_config, line, line_no):
        proxy_ip = line.get(u'proxy_ip') or raw_config[u'sip_proxy_ip']
        backup_proxy_ip = line.get(u'backup_proxy_ip') or raw_config.get(u'sip_backup_proxy_ip')
        proxy_port = line.get(u'proxy_port') or raw_config.get(u'sip_proxy_port', '5060')
        backup_proxy_port = line.get(u'backup_proxy_port') or raw_config.get(u'sip_backup_proxy_port', '5060')
        if backup_proxy_ip:
            proxy_value = u'xivo_proxies%s:SRV=%s:%s:p=0|%s:%s:p=1' % (line_no,
                            proxy_ip, proxy_port, backup_proxy_ip, backup_proxy_port)
        else:
            proxy_value = u'%s:%s' % (proxy_ip, proxy_port)
        return proxy_value

    def _add_proxies(self, raw_config):
        proxies = {}
        for line_no, line in raw_config[u'sip_lines'].iteritems():
            proxies[line_no] = self._format_proxy(raw_config, line, line_no)
        raw_config[u'XX_proxies'] = proxies

    def _add_language(self, raw_config):
        locale = raw_config.get(u'locale')
        if locale in self._LOCALE:
            raw_config[u'XX_language'] = self._LOCALE[locale]

    def _new_encryption_key(self):
        return b2a_hex(os.urandom(32))

    def _dev_specific_filename(self, dev):
        # Return the device specific filename (not pathname) of device
        fmted_mac = format_mac(dev[u'mac'], separator='')
        return fmted_mac + '.xml'

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

        self._add_fkeys(raw_config, device.get(u'model'))
        self._add_timezone(raw_config)
        self._add_proxies(raw_config)
        self._add_language(raw_config)

        update_device = False
        if raw_config.get(u'config_encryption_enabled'):
            # config encryption is enabled
            if u'X_xivo_cisco_spa_key' not in device:
                device[u'X_xivo_cisco_spa_key'] = self._new_encryption_key()
                update_device = True
            if u'X_xivo_cisco_spa_encrypted' not in device:
                device[u'X_xivo_cisco_spa_encrypted'] = False
                update_device = True
            raw_config[u'XX_key'] = device[u'X_xivo_cisco_spa_key']

        cache_path = os.path.join(self._cache_dir, filename)
        self._tpl_helper.dump(tpl, raw_config, cache_path, self._ENCODING, errors='replace')

        # encrypt configuration file if needed
        if raw_config.get(u'config_encryption_enabled') or device.get(u'X_xivo_cisco_spa_encrypted'):
            in_file = cache_path
            out_file = os.path.join(self._tftpboot_dir, filename + '.encrypted')
            logger.info('Encrypting configuration file to "%s"', out_file)
            subprocess.check_call(['openssl', 'enc', '-aes-256-cbc',
                                   '-k', device[u'X_xivo_cisco_spa_key'],
                                   '-in', in_file, '-out', out_file])

        # create a link to unencrypted config file if needed
        if not raw_config.get(u'config_encryption_enabled') or not device.get(u'X_xivo_cisco_spa_encrypted'):
            tftpboot_path = os.path.join(self._tftpboot_dir, filename)
            try:
                os.symlink(cache_path, tftpboot_path)
            except OSError, e:
                if e.errno == errno.EEXIST:
                    os.remove(tftpboot_path)
                    os.symlink(cache_path, tftpboot_path)
                else:
                    raise

        # update device if needed
        if update_device:
            self._app.dev_update(device)

    def deconfigure(self, device):
        filename = self._dev_specific_filename(device)
        cache_path = os.path.join(self._cache_dir, filename)
        tftpboot_path = os.path.join(self._tftpboot_dir, filename)
        encrypted_path = os.path.join(self._tftpboot_dir, filename + '.encrypted')
        for path in [cache_path, tftpboot_path, encrypted_path]:
            try:
                os.remove(path)
            except OSError:
                # ignore -- probably an already removed file
                pass

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
