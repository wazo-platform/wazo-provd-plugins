# -*- coding: utf-8 -*-

# Copyright 2010-2019 The Wazo Authors  (see the AUTHORS file)
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

import logging

logger = logging.getLogger('plugin.wazo-grandstream')

class GrandstreamHTTPDeviceInfoExtractor(object):

    # Grandstream Model HW GXP1405 SW 1.0.4.23 DevId 000b8240d55c
    # Grandstream Model HW GXP2200 V2.2A SW 1.0.1.33 DevId 000b82462d97
    # Grandstream Model HW GXV3240 V1.6B SW 1.0.1.27 DevId 000b82632815
    # Grandstream GXP2000 (gxp2000e.bin:1.2.5.3/boot55e.bin:1.1.6.9) DevId 000b822726c8
    # Grandstream GXW4248 (DevId c074ad18429a / c074ad18429b)
    # Grandstream GXW4216 (DevId c074ad1e8bc6)

    _UA_REGEX_LIST = [
        re.compile(r'^Grandstream Model HW (\w+)(?: V[^ ]+)? SW ([^ ]+) DevId ([^ ]+)'),
    ]

    def extract(self, request, request_type):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request):
        ua = request.getHeader('User-Agent')
        logger.debug('UA: %s',ua)
        if ua:
            return self._extract_from_ua(ua)
        return None

    def _extract_from_ua(self, ua):
        for UA_REGEX in self._UA_REGEX_LIST:
            m = UA_REGEX.match(ua)
            if m:
                raw_model, raw_version, raw_mac = m.groups()
                logger.debug('model: %s, version: %s', raw_model, raw_version)
                try:
                    mac = norm_mac(raw_mac.decode('ascii'))
                except ValueError, e:
                    logger.warning('Could not normalize MAC address "%s": %s', raw_mac, e)
                else:
                    return {u'vendor': u'Grandstream',
                            u'model': raw_model.decode('ascii'),
                            u'version': raw_version.decode('ascii'),
                            u'mac': mac}
        return None

class GrandstreamPgAssociator(BasePgAssociator):
    def __init__(self, models, version):
        BasePgAssociator.__init__(self)
        self._models = models
        self._version = version

    def _do_associate(self, vendor, model, version):
        if vendor == u'Grandstream':
            if model in self._models:
                if version == self._version:
                    return FULL_SUPPORT
                return COMPLETE_SUPPORT
            return UNKNOWN_SUPPORT
        return IMPROBABLE_SUPPORT

class BaseGrandstreamPlugin(StandardPlugin):
    _ENCODING = 'UTF-8'

    def __init__(self, app, plugin_dir, gen_cfg, spec_cfg):
        StandardPlugin.__init__(self, app, plugin_dir, gen_cfg, spec_cfg)

        self._tpl_helper = TemplatePluginHelper(plugin_dir)

        downloaders = FetchfwPluginHelper.new_downloaders(gen_cfg.get('proxies'))
        fetchfw_helper = FetchfwPluginHelper(plugin_dir, downloaders)

        self.services = fetchfw_helper.services()
        self.http_service = HTTPNoListingFileService(self._tftpboot_dir)

    http_dev_info_extractor = GrandstreamHTTPDeviceInfoExtractor()

    def configure(self, device, raw_config):
        self._check_config(raw_config)
        self._check_device(device)
        # self._check_lines_password(raw_config)
        # self._add_timezone(raw_config)
        # self._add_locale(raw_config)
        # self._add_fkeys(raw_config)
        filename = self._dev_specific_filename(device)
        tpl = self._tpl_helper.get_dev_template(filename, device)

        path = os.path.join(self._tftpboot_dir, filename)
        self._tpl_helper.dump(tpl, raw_config, path, self._ENCODING)

    def deconfigure(self, device):
        path = os.path.join(self._tftpboot_dir, self._dev_specific_filename(device))
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

    def _check_device(self, device):
        if u'mac' not in device:
            raise Exception('MAC address needed to configure device')

