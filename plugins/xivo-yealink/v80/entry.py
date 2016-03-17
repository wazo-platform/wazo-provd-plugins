# -*- coding: utf-8 -*-

# Copyright (C) 2013-2016 Avencall
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

common_globals = {}
execfile_('common.py', common_globals)

MODEL_VERSIONS = {
    u'T19P_E2': u'53.80.0.70',
    u'T21P_E2': u'52.80.0.70',
    u'T23P': u'44.80.0.70',
    u'T23G': u'44.80.0.70',
    u'T40P': u'54.80.0.95',
    u'T41P': u'36.80.0.70',
    u'T42G': u'29.80.0.70',
    u'T46G': u'28.80.0.70',
    u'T48G': u'35.80.0.70',
    u'T49G': u'51.80.0.75',
}
COMMON_FILES = [
    ('y000000000028.cfg', u'T46-28.80.0.70.rom', 'model.tpl'),
    ('y000000000029.cfg', u'T42-29.80.0.70.rom', 'model.tpl'),
    ('y000000000035.cfg', u'T48-35.80.0.70.rom', 'model.tpl'),
    ('y000000000036.cfg', u'T41-36.80.0.70.rom', 'model.tpl'),
    ('y000000000044.cfg', u'T23-44.80.0.70.rom', 'model.tpl'),
    ('y000000000051.cfg', u'T49-51.80.0.75.rom', 'model.tpl'),
    ('y000000000052.cfg', u'T21P_E2-52.80.0.70.rom', 'model.tpl'),
    ('y000000000053.cfg', u'T19P_E2-53.80.0.70.rom', 'model.tpl'),
    ('y000000000054.cfg', u'T40-54.80.0.95.rom', 'model.tpl'),
]


class YealinkPlugin(common_globals['BaseYealinkPlugin']):
    IS_PLUGIN = True

    pg_associator = common_globals['BaseYealinkPgAssociator'](MODEL_VERSIONS)

    # Yealink plugin specific stuff

    _COMMON_FILES = COMMON_FILES
