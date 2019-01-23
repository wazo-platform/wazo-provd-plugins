# -*- coding: utf-8 -*-

# Copyright 2010-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from provd.plugins import StandardPlugin, FetchfwPluginHelper
from provd.servers.tftp.service import TFTPNullService
from twisted.web.resource import NoResource
from twisted.internet import defer


_MSG = 'Test plugin for integration tests'


class TestPlugin(StandardPlugin):
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
