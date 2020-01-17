# -*- coding: utf-8 -*-

# Copyright 2010-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import errno
import logging
import os
import re
import subprocess
from copy import deepcopy
from operator import itemgetter
from xml.sax.saxutils import escape
from provd import plugins
from provd import tzinform
from provd import synchronize
from provd.devices.config import RawConfigError
from provd.devices.pgasso import BasePgAssociator, IMPROBABLE_SUPPORT, \
    PROBABLE_SUPPORT, COMPLETE_SUPPORT, FULL_SUPPORT
from provd.plugins import StandardPlugin, FetchfwPluginHelper, \
    TemplatePluginHelper
from provd.servers.http import HTTPNoListingFileService
from provd.servers.tftp.service import TFTPFileService
from provd.util import norm_mac, format_mac
from twisted.internet import defer, threads

logger = logging.getLogger('plugins.xivo-cisco-spa')


def _norm_model(raw_model):
    # Normalize a model name and return it as a unicode string. This removes
    # minus sign and make all the characters uppercase.
    return raw_model.replace('-', '').upper().decode('ascii')


class BaseCiscoDHCPDeviceInfoExtractor(object):
    _RAW_VENDORS = ['linksys', 'cisco']

    def extract(self, request, request_type):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request):
        options = request[u'options']
        logger.debug('_do_extract request: %s', request)
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
        #   "CISCO SPA122"
        #   "CISCO ATA190"
        tokens = vdi.split()
        if len(tokens) == 2:
            raw_vendor, raw_model = tokens
            if raw_vendor.lower() in self._RAW_VENDORS:
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
                    self._extract_from_args(request.args, dev_info)
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

    def _extract_from_args(self, params, dev_info):
        raw_mac = params.get('mac', [None])[0]
        if raw_mac:
            try:
                mac = norm_mac(raw_mac.decode('ascii'))
                logger.debug('Got MAC from args: %s', mac)
            except ValueError as e:
                logger.warning('Could not normalize MAC address: %s', e)
            else:
                dev_info[u'mac'] = mac


class BaseCiscoTFTPDeviceInfoExtractor(object):
    _SEPFILE_REGEX = re.compile(r'^SEP([\dA-F]{12})\.cnf\.xml$')
    _SPAFILE_REGEX = re.compile(r'^/spa(.+?)\.cfg$')
    _ATAFILE_REGEX = re.compile(r'^ATA([\dA-F]{12})\.cnf\.xml$')
    _CTLSEPFILE_REGEX = re.compile(r'^CTLSEP([\dA-F]{12})\.tlv$')

    def extract(self, request, request_type):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request):
        packet = request['packet']
        filename = packet['filename']
        for test_fun in [self._test_spafile, self._test_init, self._test_atafile]:
            dev_info = test_fun(filename)
            if dev_info:
                dev_info[u'vendor'] = u'Cisco'
                return dev_info
        return None

    def __repr__(self):
        return object.__repr__(self) + "-SPA"

    def _test_spafile(self, filename):
        # Test if filename is "/spa$PSN.cfg".
        m = self._SPAFILE_REGEX.match(filename)
        if m:
            raw_model = 'SPA' + m.group(1)
            return {u'model': _norm_model(raw_model)}
        return None

    def _test_atafile(self, filename):
        # Test if filename is "ATAMAC.cnf.xml".
        # Only the ATA190 requests this file
        m = self._ATAFILE_REGEX.match(filename)
        if m:
            return {u'model': 'ATA190'}
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
        u'SPA502G': (0, 2),
        u'SPA504G': (4, 2),
        u'SPA508G': (8, 2),
        u'SPA509G': (12, 2),
        u'SPA512G': (0, 2),
        u'SPA514G': (4, 2),
        u'SPA525G': (5, 2),
        u'SPA525G2': (5, 2),
        u'ATA190': (0,0),
    }
    _DEFAULT_LOCALE = u'en_US'
    _LANGUAGE = {
        u'de_DE': u'German',
        u'en_US': u'English',
        u'es_ES': u'Spanish',
        u'fr_FR': u'French',
        u'fr_CA': u'French',
    }
    _LOCALE = {
        u'de_DE': u'de-DE',
        u'en_US': u'en-US',
        u'es_ES': u'es-ES',
        u'fr_FR': u'fr-FR',
        u'fr_CA': u'fr-CA',
    }
    _DIRECTORY_NAME = {
        u'en_US': u'Wazo Directory',
        u'fr_FR': u'Répertoire Wazo',
    }

    def __init__(self, app, plugin_dir, gen_cfg, spec_cfg):
        StandardPlugin.__init__(self, app, plugin_dir, gen_cfg, spec_cfg)

        self._tpl_helper = TemplatePluginHelper(plugin_dir)

        downloaders = FetchfwPluginHelper.new_downloaders(gen_cfg.get('proxies'))
        if 'cisco' not in downloaders:
            logger.warning('cisco downloader not found (xivo is probably not up to date); not loading plugin packages')
        else:
            fetchfw_helper = FetchfwPluginHelper(plugin_dir, downloaders)
            self.services = fetchfw_helper.services()

        self.http_service = HTTPNoListingFileService(self._tftpboot_dir)
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
            value = funckey_dict[u'value']
            label = escape(funckey_dict.get(u'label', value))
            if funckey_type == u'speeddial':
                function = u'fnc=sd;ext=%s@$PROXY;nme=%s' % (value, label)
            elif funckey_type == u'blf':
                function = u'fnc=sd+blf+cp;sub=%s@$PROXY;nme=%s' % (value, label)
            else:
                logger.info('Unsupported funckey type: %s', funckey_type)
                continue
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
        if locale in self._LANGUAGE:
            raw_config[u'XX_language'] = self._LANGUAGE[locale]

    def _add_directory_name(self, raw_config):
        locale = raw_config.get(u'locale')
        if locale not in self._DIRECTORY_NAME:
            locale = self._DEFAULT_LOCALE
        raw_config[u'XX_directory_name'] = self._DIRECTORY_NAME[locale]

    def _add_locale(self, raw_config):
        locale = raw_config.get(u'locale')
        if locale not in self._LOCALE:
            locale = self._DEFAULT_LOCALE
        raw_config[u'XX_locale'] = self._LOCALE[locale]

    def _add_xivo_phonebook_url(self, raw_config):
        if hasattr(plugins, 'add_xivo_phonebook_url') and raw_config.get(u'config_version', 0) >= 1:
            plugins.add_xivo_phonebook_url(raw_config, u'cisco')
        else:
            self._add_xivo_phonebook_url_compat(raw_config)

    def _add_xivo_phonebook_url_compat(self, raw_config):
        hostname = raw_config.get(u'X_xivo_phonebook_ip')
        if hostname:
            raw_config[u'XX_xivo_phonebook_url'] = u'http://{hostname}/service/ipbx/web_services.php/phonebook/search/'.format(hostname=hostname)

    _SENSITIVE_FILENAME_REGEX = re.compile(r'^\w{,3}[0-9a-fA-F]{12}(?:\.cnf)?\.xml$')

    def _dev_specific_filename(self, dev):
        # Return the device specific filename (not pathname) of device
        fmted_mac = format_mac(dev[u'mac'], separator='')

        if dev.get('model', '').startswith('ATA'):
            fmted_mac = 'ATA%s.cnf' % fmted_mac.upper()

        return fmted_mac + '.xml'

    def _dev_shifted_device(self, dev):
        device2 = deepcopy(dev)
        device2[u'mac'] = device2[u'mac'][3:] + ':01'
        return device2

    def _dev_shifted_specific_filename(self, dev):
        '''Returns a device specific filename based on the shifted MAC address,
        as required by the Cisco ATA190 for the second phone port.'''
        return self._dev_specific_filename(self._dev_shifted_device(dev))

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

        self._add_fkeys(raw_config, device.get('model'))
        self._add_timezone(raw_config)
        self._add_proxies(raw_config)
        self._add_language(raw_config)
        self._add_directory_name(raw_config)
        self._add_locale(raw_config)
        self._add_xivo_phonebook_url(raw_config)

        path = os.path.join(self._tftpboot_dir, filename)
        self._tpl_helper.dump(tpl, raw_config, path, self._ENCODING, errors='replace')

        if len(raw_config[u'sip_lines']) >= 2 and device.get('model', '').startswith('ATA'):
            raw_config[u'XX_second_line_ata'] = True

            filename = self._dev_shifted_specific_filename(device)
            path = os.path.join(self._tftpboot_dir, filename)
            self._tpl_helper.dump(tpl, raw_config, path, self._ENCODING, errors='replace')

    def deconfigure(self, device):
        path = os.path.join(self._tftpboot_dir, self._dev_specific_filename(device))

        if device.get('model', '').startswith('ATA'):
            path2 = os.path.join(self._tftpboot_dir, self._dev_shifted_specific_filename(device))
            try:
                os.remove(path2)
            except OSError as e:
                logger.info('error while removing configuration file: %s', e)
        try:
            os.remove(path)
        except OSError as e:
            logger.info('error while removing configuration file: %s', e)

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

    def is_sensitive_filename(self, filename):
        return bool(self._SENSITIVE_FILENAME_REGEX.match(filename))
