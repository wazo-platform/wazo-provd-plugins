# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
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

"""Plugin for Technicolor ST2030 using the 2.74 SIP firmware."""

common_globals = {}
execfile_('common.py', common_globals)


MODEL = 'ST2030'
VERSION = '2.74'


class TechnicolorPlugin(common_globals['BaseTechnicolorPlugin']):
    IS_PLUGIN = True

    _COMMON_TEMPLATES = [('common/ST2030S.inf.tpl', 'ST2030S.inf')]
    _FILENAME_PREFIX = 'ST2030S'

    pg_associator = common_globals['BaseTechnicolorPgAssociator'](MODEL, VERSION)
