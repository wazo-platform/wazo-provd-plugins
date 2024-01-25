# Copyright 2010-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from provd.plugins import Plugin
from provd.servers.tftp.service import TFTPNullService
from twisted.web.resource import NoResource

_MSG = 'Null plugin always reject requests'


class NullPlugin(Plugin):
    IS_PLUGIN = True

    http_service = NoResource(_MSG)
    tftp_service = TFTPNullService(errmsg=_MSG)
