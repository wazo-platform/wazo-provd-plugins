# Copyright (C) 2014-2022 The Wazo Authors  (see the AUTHORS file)
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

MODEL_VERSION = {
    'SPA901': '5.1.5',
    'SPA921': '5.1.8',
    'SPA922': '6.1.5(a)',
    'SPA941': '5.1.8',
    'SPA942': '6.1.5(a)',
    'SPA962': '6.1.5(a)',
}


class CiscoPlugin(common_globals['BaseCiscoPlugin']):
    IS_PLUGIN = True

    _ENCODING = 'ISO-8859-1'
    _COMMON_FILENAMES = [
        model.lower().encode('ascii') + '.cfg' for model in MODEL_VERSION
    ]

    pg_associator = common_globals['BaseCiscoPgAssociator'](MODEL_VERSION)
