# Copyright 2010-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

try:
    from wazo_provd.plugins import Plugin
    from wazo_provd.servers.tftp.service import TFTPNullService
except ImportError:
    # Compatibility with wazo < 24.02
    from provd.plugins import Plugin
    from provd.servers.tftp.service import TFTPNullService

from twisted.web.resource import NoResource

_MSG = 'Null plugin always reject requests'


class NullPlugin(Plugin):
    IS_PLUGIN = True

    http_service = NoResource(_MSG)
    tftp_service = TFTPNullService(errmsg=_MSG)
