# -*- coding: utf-8 -*-
# Copyright 2011-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

"""Common code shared by the various wazo-gigaset plugins."""

import os
import logging
import re
import datetime
from provd.devices.pgasso import BasePgAssociator, IMPROBABLE_SUPPORT,\
    COMPLETE_SUPPORT, FULL_SUPPORT, UNKNOWN_SUPPORT
from provd.plugins import StandardPlugin, TemplatePluginHelper, FetchfwPluginHelper
from provd.util import norm_mac, format_mac
from provd import synchronize
from provd import plugins
from provd import tzinform
from provd.servers.http import HTTPNoListingFileService
from twisted.internet import defer

logger = logging.getLogger('plugin.wazo-gigaset')

VENDOR = 'Gigaset'


class GigasetDHCPDeviceInfoExtractor(object):
    _VDI = {
        'N720_DM_PRO': 'N720 DM PRO',
        'N510_IP_PRO': 'N510 IP PRO',
    }

    def extract(self, request, request_type):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request):
        options = request['options']
        if 60 in options:
            return self._extract_from_vdi(options[60])
        else:
            return None

    def _extract_from_vdi(self, vdi):
        # Vendor class identifier:
        #   "Gigaset_N720_DM_PRO"
        #   "N510_IP_PRO"

        vdi_to_check = ''
        vdi_split = vdi.split('_')

        if vdi.startswith(VENDOR):
            vdi_to_check = '_'.join(vdi_split[1:])
        else:
            vdi_to_check = '_'.join(vdi_split)

        if vdi_to_check in self._VDI:
            return {'vendor': VENDOR,
                    'model': self._VDI[vdi_to_check]}
        else:
            return None


class GigasetHTTPDeviceInfoExtractor(object):

    _UA_REGEX = re.compile(r'^(Gigaset )?(?P<model>N\d{3}.+)\/(?P<version>\d{2,3}\.\d{2,3})\.(\d{2,3})\.(\d{2,3})\.(\d{2,3});?(?P<mac>[A-F0-9]{12})?$')
    _PATH_REGEX = re.compile(r'^/\d{2}/\d{1}/(.+)$')

    def extract(self, request, request_type):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request):
        dev_info = {}

        ua = request.getHeader('User-Agent')
        if ua:
            dev_info.update(self._extract_from_ua(ua))

        return dev_info

    def _extract_from_ua(self, ua):
        # HTTP User-Agent:
        # "Gigaset N720 DM PRO/70.089.00.000.000;7C2F80CA21E4"
        # "Gigaset N720 DM PRO/70.108.00.000.000"
        # "N720-DM-PRO/70.040.00.000.000"
        # "N510 IP PRO/42.245.00.000.000;7C2F804DF9A9"
        # "N510 IP PRO/42.245.00.000.000"
        # "N510 IP PRO/42.250.00.000.000;7C2F806257D7"
        # "N510 IP PRO/42.250.00.000.000"
        m = self._UA_REGEX.search(ua)
        dev_info = {}
        if m:
            dev_info = {'vendor': VENDOR,
                        'model': m.group('model').decode('ascii'),
                        'version': m.group('version').decode('ascii')}
            if m.groupdict().get('mac'):
                dev_info['mac'] = norm_mac(m.group('mac').decode('ascii'))

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


class HTTPServiceWrapper(HTTPNoListingFileService):

    def path_preprocess(self, request):
        logger.debug('Complete path: %s', request.path)
        request.path = os.path.normpath(request.path)
        request.postpath = request.path.split('/')[1:]
        logger.debug('Preprocessed path: %s', request.path)


class BaseGigasetPlugin(StandardPlugin):
    _ENCODING = 'UTF-8'

    _TZ_GIGASET = {
        (-12, 0): 0x00,
        (-11, 0): 0x01,
        (-10, 0): 0x02,
        (-9, 0): 0x03,
        (-8, 0): 0x04,
        (-7, 0): 0x07,
        (-6, 0): 0x09,
        (-5, 0): 0x0d,
        (-4, 0): 0x10,
        (-3, 0): 0x12,
        (-2, 0): 0x16,
        (-1, 0): 0x18,
        (0, 0): 0x1a,
        (+1, 0): 0x1b,
        (+2, 0): 0x20,
        (+3, 0): 0x28,
        (+4, 0): 0x2c,
        (+4, 30): 0x2d,
        (+5, 0): 0x2f,
        (+5, 30): 0x30,
        (+5, 45): 0x31,
        (+6, 00): 0x33,
        (+6, 30): 0x35,
        (+7, 0): 0x36,
        (+8, 0): 0x38,
        (+9, 0): 0x3d,
        (+9, 30): 0x40,
        (+10, 0): 0x43,
        (+11, 0): 0x47,
        (+12, 0): 0x48,
        (+13, 0): 0x50,
    }

    def __init__(self, app, plugin_dir, gen_cfg, spec_cfg):
        StandardPlugin.__init__(self, app, plugin_dir, gen_cfg, spec_cfg)
        self._app = app

        self._tpl_helper = TemplatePluginHelper(plugin_dir)
        downloaders = FetchfwPluginHelper.new_downloaders(gen_cfg.get('proxies'))
        fetchfw_helper = FetchfwPluginHelper(plugin_dir, downloaders)

        self.services = fetchfw_helper.services()
        self.http_service = HTTPServiceWrapper(self._tftpboot_dir)

    dhcp_dev_info_extractor = GigasetDHCPDeviceInfoExtractor()
    http_dev_info_extractor = GigasetHTTPDeviceInfoExtractor()

    def _check_device(self, device):
        if 'ip' not in device:
            raise Exception('IP address needed for Gigaset configuration')

    def _check_config(self, raw_config):
        pass

    def _dev_specific_filename(self, device):
        # Return the device specific filename (not pathname) of device
        fmted_mac = format_mac(device['mac'], separator='', uppercase=True)
        return fmted_mac + '.xml'

    def _add_phonebook(self, raw_config):
        uuid_format = u'{scheme}://{hostname}:{port}/0.1/directories/lookup/default/gigaset/{user_uuid}?'
        plugins.add_xivo_phonebook_url_from_format(raw_config, uuid_format)

    def _add_timezone_code(self, raw_config):
        timezone = raw_config.get('timezone', 'Etc/UTC')
        tz_db = tzinform.TextTimezoneInfoDB()
        tz_info = tz_db.get_timezone_info(timezone)['utcoffset'].as_hms
        offset_hour = tz_info[0]
        offset_minutes = tz_info[1]
        raw_config['XX_timezone_code'] = self._TZ_GIGASET[(offset_hour, offset_minutes)]

    def _add_xx_vars(self, device, raw_config):
        raw_config['XX_mac_addr'] = format_mac(device['mac'], separator='', uppercase=True)

        cur_datetime = datetime.datetime.now()
        raw_config['XX_version_date'] = cur_datetime.strftime('%d%m%y%H%M')

        if 'dns_enabled' in raw_config:
            ip = raw_config['dns_ip']
            ip_str = '0x' + ''.join(['%x' % int(p) for p in ip.split('.')])
            raw_config['XX_dns_ip_hex'] = ip_str

        self._add_timezone_code(raw_config)

    def _add_sip_info(self, raw_config):
        if '1' in raw_config['sip_lines']:
            line = raw_config['sip_lines']['1']
            raw_config['sip_proxy_ip'] = line['proxy_ip']
            raw_config['sip_proxy_port'] = line.get('proxy_port', 5060)
            raw_config['sip_registrar_ip'] = line.get('registrar_ip')
            raw_config['sip_registrar_port'] = line.get('registrar_port', 5060)

    def configure(self, device, raw_config):
        self._check_config(raw_config)
        self._check_device(device)
        filename = self._dev_specific_filename(device)
        tpl = self._tpl_helper.get_dev_template(filename, device)

        self._add_sip_info(raw_config)
        self._add_xx_vars(device, raw_config)
        self._add_phonebook(raw_config)

        path = os.path.join(self._tftpboot_dir, filename)
        self._tpl_helper.dump(tpl, raw_config, path, self._ENCODING)

    def deconfigure(self, device):
        path = os.path.join(self._tftpboot_dir, self._dev_specific_filename(device))
        try:
            os.remove(path)
        except OSError as e:
            logger.info('error while removing configuration file: %s', e)

    def is_sensitive_filename(self, filename):
        return bool(self._SENSITIVE_FILENAME_REGEX.match(filename))

    _SENSITIVE_FILENAME_REGEX = re.compile(r'^[0-9A-F]{12}\.xml$')

    def synchronize(self, device, raw_config):
        return synchronize.standard_sip_synchronize(device)
