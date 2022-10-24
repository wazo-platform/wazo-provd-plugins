# Copyright 2013-2022 The Wazo Authors  (see the AUTHORS file)
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
    'C58',
    'C62',
]
COMMON_FILES = {
    'f0C00580000.cfg': ('C58', 'C58_V2_3_431_247T20140605184312.z', 'model.tpl'),
    'f0C00620000.cfg': ('C62', '2012070649327421.z', 'model.tpl'),
}


class FanvilPlugin(common['BaseFanvilPlugin']):
    IS_PLUGIN = True

    _COMMON_FILES = COMMON_FILES
    _LOCALE = {
        'de_DE': 'de',
        'es_ES': 'es',
        'fr_FR': 'fr',
        'fr_CA': 'fr',
        'it_IT': 'it',
        'nl_NL': 'nl',
        'en_US': 'en',
    }
    _TZ_INFO = {
        -12: [('UCT_-12', 0)],
        -11: [('UCT_-11', 1)],
        -10: [('UCT_-10', 2)],
        -9: [('UCT_-09', 3)],
        -8: [('UCT_-08', 4)],
        -7: [('UCT_-07', 5)],
        -6: [('UCT_-06', 8)],
        -5: [('UCT_-05', 12)],
        -4: [('UCT_-04', 15)],
        -3: [('UCT_-03', 19)],
        -2: [('UCT_-02', 22)],
        -1: [('UCT_-01', 23)],
        0: [('UCT_000', 25)],
        1: [('MET_001', 27)],
        2: [('EET_002', 32)],
        3: [('IST_003', 38)],
        4: [('UCT_004', 43)],
        5: [('UCT_005', 46)],
        6: [('UCT_006', 50)],
        7: [('UCT_007', 54)],
        8: [('CST_008', 56)],
        9: [('JST_009', 61)],
        10: [('UCT_010', 66)],
        11: [('UCT_011', 71)],
        12: [('UCT_012', 72)],
    }

    pg_associator = common['BaseFanvilPgAssociator'](MODELS)
    http_dev_info_extractor = common['BaseFanvilHTTPDeviceInfoExtractor'](_COMMON_FILES)
