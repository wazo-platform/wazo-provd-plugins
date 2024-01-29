# Copyright 2010-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

try:
    from wazo_provd.plugins import StandardPlugin
    from wazo_provd.servers.http import HTTPNoListingFileService
    from wazo_provd.servers.tftp.service import TFTPFileService
except ImportError:
    # Compatibility with wazo < 24.02
    from provd.plugins import StandardPlugin
    from provd.servers.http import HTTPNoListingFileService
    from provd.servers.tftp.service import TFTPFileService


class ZeroPlugin(StandardPlugin):
    IS_PLUGIN = True

    def __init__(self, app, plugin_dir, gen_cfg, spec_cfg):
        super().__init__(app, plugin_dir, gen_cfg, spec_cfg)
        self.tftp_service = TFTPFileService(self._tftpboot_dir)
        self.http_service = HTTPNoListingFileService(self._tftpboot_dir)
