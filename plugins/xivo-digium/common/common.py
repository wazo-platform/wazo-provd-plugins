# -*- coding: UTF-8 -*-

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

import logging
import os
import re
from provd import synchronize
from provd.util import norm_mac, format_mac
from provd.plugins import StandardPlugin, FetchfwPluginHelper, \
    TemplatePluginHelper
from provd.devices.pgasso import IMPROBABLE_SUPPORT, PROBABLE_SUPPORT,\
    COMPLETE_SUPPORT, FULL_SUPPORT, BasePgAssociator
from provd.servers.http import HTTPNoListingFileService
from twisted.internet import defer, threads


logger = logging.getLogger('plugin.xivo-digium')


class DigiumDHCPDeviceInfoExtractor(object):

    _VDI_REGEX = re.compile(r'^digium_(D\d\d)_([\d_]+)$')

    def extract(self, request, request_type):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request):
        options = request['options']
        if 60 in options:
            return self._extract_from_vdi(options[60])

    def _extract_from_vdi(self, vdi):
        # Vendor Class Identifier:
        #   digium_D40_1_0_5_46476
        #   digium_D40_1_1_0_0_48178
        #   digium_D70_1_0_5_46476
        #   digium_D70_1_1_0_0_48178
        match = self._VDI_REGEX.match(vdi)
        if match:
            model = match.group(1).decode('ascii')
            fw_version = match.group(2).replace('_', '.').decode('ascii')
            dev_info = {u'vendor': u'Digium',
                        u'model': model,
                        u'version': fw_version}
            return dev_info


class DigiumHTTPDeviceInfoExtractor(object):

    _PATH_REGEX = re.compile(r'^/Digium/(?:([a-fA-F\d]{12})\.cfg)?')

    def extract(self, request, request_type):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request):
        match = self._PATH_REGEX.match(request.path)
        if match:
            dev_info = {u'vendor': u'Digium'}
            raw_mac = match.group(1)
            if raw_mac and raw_mac != '000000000000':
                mac = norm_mac(raw_mac.decode('ascii'))
                dev_info[u'mac'] = mac
            return dev_info


class DigiumPgAssociator(BasePgAssociator):

    _MODELS = [u'D40', u'D50', u'D70']

    def __init__(self, version):
        BasePgAssociator.__init__(self)
        self._version = version

    def _do_associate(self, vendor, model, version):
        if vendor == u'Digium':
            if model in self._MODELS:
                if version == self._version:
                    return FULL_SUPPORT
                return COMPLETE_SUPPORT
            return PROBABLE_SUPPORT
        return IMPROBABLE_SUPPORT


class BaseDigiumPlugin(StandardPlugin):

    _ENCODING = 'UTF-8'
    _CONTACT_TEMPLATE = 'contact.tpl'

    def __init__(self, app, plugin_dir, gen_cfg, spec_cfg):
        StandardPlugin.__init__(self, app, plugin_dir, gen_cfg, spec_cfg)

        self._tpl_helper = TemplatePluginHelper(plugin_dir)
        self._digium_dir = os.path.join(self._tftpboot_dir, 'Digium')

        downloaders = FetchfwPluginHelper.new_downloaders(gen_cfg.get('proxies'))
        fetchfw_helper = FetchfwPluginHelper(plugin_dir, downloaders)

        self.services = fetchfw_helper.services()
        self.http_service = HTTPNoListingFileService(self._tftpboot_dir)

    dhcp_dev_info_extractor = DigiumDHCPDeviceInfoExtractor()

    http_dev_info_extractor = DigiumHTTPDeviceInfoExtractor()

    def configure(self, device, raw_config):
        self._check_device(device)

        filename = self._dev_specific_filename(device)
        contact_filename = self._dev_contact_filename(device)

        tpl = self._tpl_helper.get_dev_template(filename, device)
        contact_tpl = self._tpl_helper.get_template(self._CONTACT_TEMPLATE)

        raw_config['XX_mac'] = self._format_mac(device)
        raw_config['XX_main_proxy_ip'] = self._get_main_proxy_ip(raw_config)
        raw_config['XX_funckeys'] = self._transform_funckeys(raw_config)

        path = os.path.join(self._digium_dir, filename)
        contact_path = os.path.join(self._digium_dir, contact_filename)
        self._tpl_helper.dump(tpl, raw_config, path, self._ENCODING)
        self._tpl_helper.dump(contact_tpl, raw_config, contact_path, self._ENCODING)

    def deconfigure(self, device):
        filenames = [
            self._dev_specific_filename(device),
            self._dev_contact_filename(device)
        ]

        for filename in filenames:
            path = os.path.join(self._digium_dir, filename)
            try:
                os.remove(path)
            except OSError as e:
                logger.info('error while removing file %s: %s', (path, e))

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

    def _check_device(self, device):
        if u'mac' not in device:
            raise Exception('MAC address needed to configure device')

    def _get_main_proxy_ip(self, raw_config):
        if raw_config[u'sip_lines']:
            line_no = min(int(x) for x in raw_config[u'sip_lines'].keys())
            line_no = str(line_no)
            return raw_config[u'sip_lines'][line_no][u'proxy_ip']
        else:
            return raw_config[u'ip']

    def _format_mac(self, device):
         return format_mac(device[u'mac'], separator='', uppercase=False)

    def _dev_specific_filename(self, device):
        filename = '%s.cfg' % self._format_mac(device)
        return filename

    def _dev_contact_filename(self, device):
        contact_filename = '%s-contacts.xml' % self._format_mac(device)
        return contact_filename

    def _transform_funckeys(self, raw_config):
        return dict(
            (int(k), v) for k, v in raw_config['funckeys'].iteritems()
        )

