# -*- coding: utf-8 -*-

# Copyright 2013-2018 The Wazo Authors  (see the AUTHORS file)
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

common = {}
execfile_('common.py', common)

MODELS = [
    u'C58',
    u'C62',
]
COMMON_FILES = [
    ('f0C00580000.cfg', u'C58_V2_3_431_247T20140605184312.z', 'model.tpl'),
    ('f0C00620000.cfg', u'2012070649327421.z', 'model.tpl'),
]


class FanvilPlugin(common['BaseFanvilPlugin']):
    IS_PLUGIN = True

    _COMMON_FILES = COMMON_FILES
    _LOCALE = {
        u'de_DE': 'de',
        u'es_ES': 'es',
        u'fr_FR': 'fr',
        u'fr_CA': 'fr',
        u'it_IT': 'it',
        u'nl_NL': 'nl',
        u'en_US': 'en'
    }
    _TZ_INFO = {
        -12: [(u'UCT_-12', 0)],
        -11: [(u'UCT_-11', 1)],
        -10: [(u'UCT_-10', 2)],
        -9: [(u'UCT_-09', 3)],
        -8: [(u'UCT_-08', 4)],
        -7: [(u'UCT_-07', 5)],
        -6: [(u'UCT_-06', 8)],
        -5: [(u'UCT_-05', 12)],
        -4: [(u'UCT_-04', 15)],
        -3: [(u'UCT_-03', 19)],
        -2: [(u'UCT_-02', 22)],
        -1: [(u'UCT_-01', 23)],
        0: [(u'UCT_000', 25)],
        1: [(u'MET_001', 27)],
        2: [(u'EET_002', 32)],
        3: [(u'IST_003', 38)],
        4: [(u'UCT_004', 43)],
        5: [(u'UCT_005', 46)],
        6: [(u'UCT_006', 50)],
        7: [(u'UCT_007', 54)],
        8: [(u'CST_008', 56)],
        9: [(u'JST_009', 61)],
        10: [(u'UCT_010', 66)],
        11: [(u'UCT_011', 71)],
        12: [(u'UCT_012', 72)],
    }

    pg_associator = common['BaseFanvilPgAssociator'](MODELS)
