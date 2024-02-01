# Copyright 2010-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from provd.plugins import FetchfwPluginHelper, StandardPlugin
from provd.servers.tftp.service import TFTPNullService
from twisted.internet import defer
from twisted.web.resource import NoResource

_MSG = 'Test plugin with legacy import for integration tests'


class TestPluginLegacyImport(StandardPlugin):
    IS_PLUGIN = True

    http_service = NoResource(_MSG)
    tftp_service = TFTPNullService(errmsg=_MSG)

    def __init__(self, app, plugin_dir, gen_cfg, spec_cfg):
        StandardPlugin.__init__(self, app, plugin_dir, gen_cfg, spec_cfg)

        downloaders = FetchfwPluginHelper.new_downloaders(gen_cfg.get('proxies'))
        fetchfw_helper = FetchfwPluginHelper(plugin_dir, downloaders)

        self.services = fetchfw_helper.services()

    def synchronize(self, device, raw_config):
        return defer.succeed(None)
