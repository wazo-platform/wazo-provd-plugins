# Copyright (C) 2011-2022 The Wazo Authors  (see the AUTHORS file)
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

"""Plugin for the Jitsi softphone in version 1.x.

"""


# provisioning url to use in Jitsi: http://<provd_ip:provd_port>/jitsi?uuid=${uuid}

import logging
import os.path
import re
from provd.devices.config import RawConfigError
from provd.devices.pgasso import IMPROBABLE_SUPPORT, PROBABLE_SUPPORT,\
    FULL_SUPPORT, BasePgAssociator
from provd.plugins import StandardPlugin, TemplatePluginHelper
from provd.util import is_normed_uuid, norm_uuid
from twisted.internet import defer
from twisted.web.resource import Resource

logger = logging.getLogger('plugin.xivo-jitsi')


class JitsiHTTPDeviceInfoExtractor:
    _UA_REGEX = re.compile(r'^Jitsi/(\S+)$')
    
    def extract(self, request, request_type):
        return defer.succeed(self._do_extract(request))
    
    def _do_extract(self, request):
        ua = request.getHeader('User-Agent')
        if ua:
            dev_info = self._extract_from_ua(ua)
            if dev_info:
                self._extract_from_args(request.args, dev_info)
                return dev_info
        return None
    
    def _extract_from_ua(self, ua):
        # HTTP User-Agent:
        #   "Jitsi/1.0-beta1-nightly.build.3408"
        m = self._UA_REGEX.match(ua)
        if m:
            raw_version = m.group(1)
            return {'vendor': 'Jitsi',
                    'model': 'Jitsi',
                    'version': raw_version.decode('ascii')}
        return None
    
    def _extract_from_args(self, args, dev_info):
        if 'uuid' in args:
            try:
                dev_info['uuid'] = norm_uuid(args['uuid'][0].decode('ascii'))
            except ValueError as e:
                logger.warning('Could not normalize UUID: %s', e)


class JitsiPgAssociator(BasePgAssociator):
    def _do_associate(self, vendor, model, version):
        if vendor == model == 'Jitsi':
            if version.startswith('1.'):
                return FULL_SUPPORT
            return PROBABLE_SUPPORT
        return IMPROBABLE_SUPPORT


class JitsiHTTPService(Resource):
    def __init__(self, tftpboot_dir):
        Resource.__init__(self)
        self._tftpboot_dir = tftpboot_dir
    
    def render_POST(self, request):
        try:
            uuid = request.args['uuid'][0]
        except KeyError:
            logger.warning('No UUID in args: %s', request.args)
            request.setResponseCode(400)
            request.setHeader('Content-Type', 'text/plain; charset=ascii')
            return 'missing uuid'
        else:
            if not is_normed_uuid(uuid):
                # non normalized uuid can lead to security issue
                logger.warning('Non normalized uuid: %s', uuid)
                request.setResponseCode(400)
                request.setHeader('Content-Type', 'text/plain; charset=ascii')
                return 'invalid uuid'
            else:
                file = os.path.join(self._tftpboot_dir, uuid)
                try:
                    with open(file) as fobj:
                        content = fobj.read()
                except EnvironmentError as e:
                    logger.warning('Error while reading file %s: %s', file, e)
                    request.setResponseCode(404)
                    request.setHeader('Content-Type', 'text/plain; charset=ascii')
                    return 'not found/error while reading'
                else:
                    request.setResponseCode(200)
                    request.setHeader('Content-Type', 'text/plain; charset=UTF-8')
                    return content


class JitsiPlugin(StandardPlugin):
    IS_PLUGIN = True
    
    _ENCODING = 'UTF-8'
    
    def __init__(self, app, plugin_dir, gen_cfg, spec_cfg):
        StandardPlugin.__init__(self, app, plugin_dir, gen_cfg, spec_cfg)
        
        self._tpl_helper = TemplatePluginHelper(plugin_dir)
        
        root_resource = Resource()
        root_resource.putChild('jitsi', JitsiHTTPService(self._tftpboot_dir))
        self.http_service = root_resource
    
    http_dev_info_extractor = JitsiHTTPDeviceInfoExtractor()
    
    pg_associator = JitsiPgAssociator()
    
    def _device_config_filename(self, device):
        # Return the device specific filename (not pathname) of device
        return device['uuid']
    
    def _check_config(self, raw_config):
        if 'http_port' not in raw_config:
            raise RawConfigError('only support configuration via HTTP')
    
    def _check_device(self, device):
        if 'uuid' not in device:
            raise Exception('UUID needed for device configuration')
        if not is_normed_uuid(device['uuid']):
            # non normalized uuid can lead to security issue
            raise Exception('non normalized UUID: %s', device['uuid'])
    
    def configure(self, device, raw_config):
        self._check_config(raw_config)
        self._check_device(device)
        filename = self._device_config_filename(device)
        tpl = self._tpl_helper.get_dev_template(filename, device)
        
        path = os.path.join(self._tftpboot_dir, filename)
        self._tpl_helper.dump(tpl, raw_config, path, self._ENCODING)
    
    def deconfigure(self, device):
        path = os.path.join(self._tftpboot_dir, self._device_config_filename(device))
        try:
            os.remove(path)
        except OSError as e:
            logger.warning('error while deconfiguring device: %s', e)

    def get_remote_state_trigger_filename(self, device):
        if 'uuid' not in device:
            return None

        return self._device_config_filename(device)
