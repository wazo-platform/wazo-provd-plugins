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

"""Common code shared by the various xivo-zenitel plugins.

"""
from __future__ import annotations

import logging
import os.path
import re
import urllib.error
import urllib.parse
import urllib.request
from operator import itemgetter
from typing import Dict

from provd.devices.config import RawConfigError
from provd.devices.pgasso import (
    IMPROBABLE_SUPPORT,
    COMPLETE_SUPPORT,
    UNKNOWN_SUPPORT,
    BasePgAssociator,
)
from provd.plugins import StandardPlugin, TemplatePluginHelper, FetchfwPluginHelper
from provd.servers.tftp.service import TFTPFileService
from provd.services import JsonConfigPersister, PersistentConfigureServiceDecorator
from provd.util import norm_mac, format_mac
from provd.devices.ident import RequestType
from twisted.internet import defer, threads

logger = logging.getLogger('plugin.xivo-zenitel')


class BaseZenitelTFTPDeviceInfoExtractor:
    _FILENAME_REGEX = re.compile(r'^ipst_config((?:_\w\w){6})?\.cfg$')

    def extract(self, request: dict, request_type: RequestType):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request: dict):
        # filename:
        #   "ipst_config.cfg"
        #   "ipst_config_01_02_03_04_05_ab.cfg"
        filename = request['packet']['filename']
        m = self._FILENAME_REGEX.match(filename)
        if m:
            dev_info = {'vendor': 'Zenitel', 'model': 'IP station'}
            raw_mac = m.group(1)
            if raw_mac:
                raw_mac = raw_mac.replace('_', '')
                try:
                    dev_info['mac'] = norm_mac(raw_mac)
                except ValueError as e:
                    logger.warning('Could not normalize MAC address: %s', e)
            return dev_info
        return None


class BaseZenitelPgAssociator(BasePgAssociator):
    def _do_associate(self, vendor, model, version):
        if vendor == 'Zenitel':
            if model == 'IP station':
                return COMPLETE_SUPPORT
            else:
                return UNKNOWN_SUPPORT
        else:
            return IMPROBABLE_SUPPORT


class ZenitelConfigureService:
    _URI = 'https://alphasupport.zenitel.com/alphawiki/'

    def __init__(self, auth_downloader, username, password):
        # username and password can be None
        self._auth_downloader = auth_downloader
        self._p_username = username
        self._p_password = password
        self._update_dler()

    def _update_dler(self):
        if self._p_username and self._p_password:
            self._auth_downloader.add_password(
                None, self._URI, self._p_username, self._p_password
            )
        else:
            # XXX this use some knowledge of the underlying implementation:
            # * AuthDownloader.add_password is just a wrapper around
            #   urllib2.HTTPPasswordManager.add_password
            # * urllib2.HTTPPaswordManager accept (None, None) as username
            #   and password
            self._auth_downloader.add_password(None, self._URI, None, None)

    def get(self, name):
        try:
            return getattr(self, '_p_' + name)
        except AttributeError as e:
            raise KeyError(e)

    def set(self, name, value):
        attrname = '_p_' + name
        if hasattr(self, attrname):
            setattr(self, attrname, value)
            self._update_dler()
        else:
            raise KeyError(name)

    description = [
        ('username', 'The username used to download files on the alphawiki'),
        ('password', 'The password used to download files on the alphawiki'),
    ]

    description_fr = [
        (
            'username',
            "Le nom d'utilisateur pour télécharger les fichiers sur le alphawiki",
        ),
        ('password', 'Le mot de passe pour télécharger les fichiers sur le alphawiki'),
    ]


class BaseZenitelPlugin(StandardPlugin):
    _ENCODING = 'UTF-8'
    _VALID_FUNCKEY_NO = ['1', '2', '3']

    def __init__(self, app, plugin_dir, gen_cfg, spec_cfg):
        super().__init__(app, plugin_dir, gen_cfg, spec_cfg)

        self._tpl_helper = TemplatePluginHelper(plugin_dir)

        downloaders = FetchfwPluginHelper.new_downloaders(gen_cfg.get('proxies'))
        fetchfw_helper = FetchfwPluginHelper(plugin_dir, downloaders)

        cfg_service = ZenitelConfigureService(
            downloaders['auth'], spec_cfg.get('username'), spec_cfg.get('password')
        )
        persister = JsonConfigPersister(
            os.path.join(self._plugin_dir, 'var', 'config.json')
        )
        cfg_service = PersistentConfigureServiceDecorator(cfg_service, persister)

        self.services = {'configure': cfg_service, 'install': fetchfw_helper}
        self.tftp_service = TFTPFileService(self._tftpboot_dir)

    tftp_dev_info_extractor = BaseZenitelTFTPDeviceInfoExtractor()

    pg_associator = BaseZenitelPgAssociator()

    def _add_sip_section_info(self, raw_config):
        if '1' in raw_config['sip_lines']:
            line = raw_config['sip_lines']['1']
            raw_config['XX_sip'] = True
            raw_config['XX_nick_name'] = line['display_name']
            raw_config['XX_sip_id'] = line['username']
            raw_config['XX_domain'] = line.get('proxy_ip') or raw_config['sip_proxy_ip']
            raw_config['XX_domain2'] = line.get('backup_proxy_ip') or raw_config.get(
                'backup_proxy_ip', ''
            )
            raw_config['XX_auth_user'] = line['auth_username']
            raw_config['XX_auth_pwd'] = line['password']

    def _add_fkeys(self, raw_config):
        lines = []
        for funckey_no, funckey_dict in sorted(
            iter(raw_config['funckeys'].items()), key=itemgetter(0)
        ):
            if funckey_no in self._VALID_FUNCKEY_NO:
                if funckey_dict['type'] == 'speeddial':
                    exten = funckey_dict['value']
                    lines.append(f'speeddial_{funckey_no}_c1={exten}')
                else:
                    logger.info('Unsupported funckey type: %s', funckey_dict['type'])
            else:
                logger.info('Out of range funckey no: %s', funckey_no)
        raw_config['XX_fkeys'] = '\n'.join(' ' + s for s in lines)

    def _dev_specific_filename(self, device: Dict[str, str]) -> str:
        # Return the device specific filename (not pathname) of device
        formatted_mac = format_mac(device['mac'], separator='_', uppercase=False)
        return f'ipst_config_{formatted_mac}.cfg'

    def _check_config(self, raw_config):
        if 'tftp_port' not in raw_config:
            raise RawConfigError('only support configuration via TFTP')

    def _check_device(self, device):
        if 'mac' not in device:
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
        except OSError as e:
            # ignore
            logger.info('error while removing file: %s', e)

    def _do_synchronize(self, ip):
        # XXX could use twisted native http stuff one day...
        url = f"http://{ip}/goform/zForm_send_cmd"
        pwd_manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        pwd_manager.add_password(None, url, 'admin', 'alphaadmin')
        basic_auth_handler = urllib.request.HTTPBasicAuthHandler(pwd_manager)
        opener = urllib.request.build_opener(basic_auth_handler)
        fobj = opener.open(url, 'message=Reboot', 15)
        try:
            fobj.read()
        except Exception as e:
            logger.info('Exception during read from Zenitel synchronize: %s', e)
        finally:
            fobj.close()

    def synchronize(self, device, raw_config):
        try:
            ip = device['ip']
        except KeyError:
            return defer.fail(Exception('IP address needed for device synchronization'))
        else:
            return threads.deferToThread(self._do_synchronize, ip)
