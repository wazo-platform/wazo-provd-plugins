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

"""Plugin for Technicolor TB30 using the 1.74.0 SIP firmware."""

common_globals = {}
execfile_('common.py', common_globals)


MODEL = 'TB30'
VERSION = '1.74.0'


class TechnicolorPlugin(common_globals['BaseTechnicolorPlugin']):
    IS_PLUGIN = True

    _COMMON_TEMPLATES = [('common/TB30S.inf.tpl', 'TB30S.inf')]
    _FILENAME_PREFIX = 'TB30S'

    pg_associator = common_globals['BaseTechnicolorPgAssociator'](MODEL, VERSION)
