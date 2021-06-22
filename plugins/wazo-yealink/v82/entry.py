# -*- coding: utf-8 -*-

# Copyright 2013-2017 The Wazo Authors  (see the AUTHORS file)
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

import os

common_globals = {}
execfile_('common.py', common_globals)

MODEL_VERSIONS = {
    u'T19P_E2': u'53.82.0.20',
    u'T21P_E2': u'52.82.0.20',
    u'T23P': u'44.82.0.20',
    u'T23G': u'44.82.0.20',
    u'T27P': u'45.82.0.20',
    u'T27G': u'69.82.0.20',
    u'T29G': u'46.82.0.20',
    u'T40P': u'54.82.0.20',
    u'T40G': u'76.82.0.20',
    u'T41P': u'36.82.0.20',
    u'T41S': u'66.82.0.20',
    u'T42G': u'29.82.0.20',
    u'T42S': u'66.82.0.20',
    u'T46G': u'28.82.0.20',
    u'T46S': u'66.82.0.20',
    u'T48G': u'35.82.0.20',
    u'T48S': u'66.82.0.20',
}

COMMON_FILES = [
    ('y000000000028.cfg', u'T46-28.82.0.20.rom', 'model.tpl'),
    ('y000000000029.cfg', u'T42-29.82.0.20.rom', 'model.tpl'),
    ('y000000000035.cfg', u'T48-35.82.0.20.rom', 'model.tpl'),
    ('y000000000036.cfg', u'T41-36.82.0.20.rom', 'model.tpl'),
    ('y000000000044.cfg', u'T23-44.82.0.20.rom', 'model.tpl'),
    ('y000000000045.cfg', u'T27-45.82.0.20.rom', 'model.tpl'),
    ('y000000000069.cfg', u'T27G-69.82.0.20.rom', 'model.tpl'),
    ('y000000000046.cfg', u'T29-46.82.0.20.rom', 'model.tpl'),
    ('y000000000052.cfg', u'T21P_E2-52.82.0.20.rom', 'model.tpl'),
    ('y000000000053.cfg', u'T19P_E2-53.82.0.20.rom', 'model.tpl'),
    ('y000000000054.cfg', u'T40-54.82.0.20.rom', 'model.tpl'),
    ('y000000000076.cfg', u'T40G-76.82.0.20.rom', 'model.tpl'),
    ('y000000000066.cfg', u'T46S(T48S,T42S,T41S)-66.82.0.20.rom', 'model.tpl'),
]


class YealinkPlugin(common_globals['BaseYealinkPlugin']):
    IS_PLUGIN = True

    pg_associator = common_globals['BaseYealinkPgAssociator'](MODEL_VERSIONS)

    # Yealink plugin specific stuff

    _COMMON_FILES = COMMON_FILES
