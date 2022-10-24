# Copyright (C) 2013-2022 The Wazo Authors  (see the AUTHORS file)
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

MODEL = 'ST2022'
VERSION = '4.78.1'


class TechnicolorPlugin(common_globals['BaseTechnicolorPlugin']):
    IS_PLUGIN = True

    _COMMON_TEMPLATES = [('common/ST2022S.inf.tpl', 'ST2022S.inf')]
    _FILENAME_PREFIX = 'ST2022S'
    _NB_FKEYS = 5
    _NB_LINES = 2

    pg_associator = common_globals['BaseTechnicolorPgAssociator'](MODEL, VERSION)
