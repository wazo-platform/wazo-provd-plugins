# -*- coding: utf-8 -*-

# Copyright (C) 2013-2015 Avencall
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

common_globals = {}
execfile_('common.py', common_globals)

logger = logging.getLogger('plugin.xivo-yealink')

MODEL_VERSIONS = {
    u'T19P_E2': u'53.80.0.60',
    u'T21P_E2': u'52.80.0.60',
    u'T41P': u'36.80.0.60',
    u'T42G': u'29.80.0.60',
    u'T46G': u'28.80.0.60',
    u'T48G': u'35.80.0.60',
}
MODEL_SIP_ACCOUNTS = {
    u'T19P_E2': 1,
    u'T21P_E2': 2,
    u'T41P': 6,
    u'T42G': 12,
    u'T46G': 16,
    u'T48G': 16,
}
COMMON_FILES = [
    ('y000000000028.cfg', u'28.80.0.60.rom', 'model.tpl'),
    ('y000000000029.cfg', u'29.80.0.60.rom', 'model.tpl'),
    ('y000000000035.cfg', u'35.80.0.60.rom', 'model.tpl'),
    ('y000000000036.cfg', u'36.80.0.60.rom', 'model.tpl'),
    ('y000000000052.cfg', u'52.80.0.60.rom', 'model.tpl'),
    ('y000000000053.cfg', u'53.80.0.60.rom', 'model.tpl'),
]


class YealinkPlugin(common_globals['BaseYealinkPlugin']):
    IS_PLUGIN = True

    pg_associator = common_globals['BaseYealinkPgAssociator'](MODEL_VERSIONS)

    # Yealink plugin specific stuff

    _COMMON_FILES = COMMON_FILES

    def _get_sip_accounts(self, model):
        return MODEL_SIP_ACCOUNTS.get(model)
