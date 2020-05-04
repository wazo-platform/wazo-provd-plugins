# -*- coding: utf-8 -*-

# Copyright (C) 2020 Wazo Authors
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
    u'UC926': u'2.0.4.6.41',
    u'UC924': u'2.0.4.6.41',
    u'UC923': u'2.0.4.6.41',
    u'UC912': u'2.0.4.6.41',
    u'UC912G': u'2.0.4.6.41',
    u'UC903': u'2.0.4.6.41',
    u'UC902': u'2.0.4.6.41',
}

COMMON_FILES = [
    ('cfg0010.xml', 'model.tpl'),  # UC926
    ('cfg0012.xml', 'model.tpl'),  # UC924
    ('cfg0013.xml', 'model.tpl'),  # UC923
    ('cfg0016.xml', 'model.tpl'),  # UC903
    ('cfg0017.xml', 'model.tpl'),  # UC902
    ('cfg0019.xml', 'model.tpl'),  # UC912 / UC912G / UC912E
]


class HtekPlugin(common_globals['BaseHtekPlugin']):
    IS_PLUGIN = True

    pg_associator = common_globals['BaseHtekPgAssociator'](MODEL_VERSIONS)

    # Htek plugin specific stuff

    _COMMON_FILES = COMMON_FILES
