# Copyright 2014-2023 The Wazo Authors  (see the AUTHORS file)
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

PSN = [
    '301',
    '303',
    '501G',
    '502G',
    '504G',
    '508G',
    '509G',
    '512G',
    '514G',
    '525G',
    '525G2',
]
MODELS = ['SPA' + psn for psn in PSN]
MODEL_VERSION = {model: '7.5.5' for model in MODELS}


class CiscoPlugin(common_globals['BaseCiscoPlugin']):
    IS_PLUGIN = True
    # similar to spa508G.cfg (G is uppercase)
    _COMMON_FILENAMES = [''.join(['spa', psn, '.cfg']) for psn in PSN]

    pg_associator = common_globals['BaseCiscoPgAssociator'](MODEL_VERSION)
