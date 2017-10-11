# -*- coding: utf-8 -*-

# Copyright (C) 2017 Wazo Authors
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
    u'UC926': u'2.0.4.2.19',
    u'UC903': u'2.0.4.2.19',
}

COMMON_FILES = [
    ('cfg0010.xml', u'fw926.rom', 'model.tpl'),
    ('cfg0016.xml', u'fw903.rom', 'model.tpl'),
]


class HtekPlugin(common_globals['BaseHtekPlugin']):
    IS_PLUGIN = True

    pg_associator = common_globals['BaseHtekPgAssociator'](MODEL_VERSIONS)

    # Htek plugin specific stuff

    _COMMON_FILES = COMMON_FILES
