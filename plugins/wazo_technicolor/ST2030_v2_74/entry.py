# Copyright 2013-2023 The Wazo Authors  (see the AUTHORS file)
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
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypedDict
    from ..common.common import (  # noqa: F401
        BaseTechnicolorPlugin,
        BaseTechnicolorPgAssociator,
    )

    class CommonGlobalsDict(TypedDict):
        BaseTechnicolorPlugin: type[BaseTechnicolorPlugin]
        BaseTechnicolorPgAssociator: type[BaseTechnicolorPgAssociator]


common_globals: CommonGlobalsDict = {}  # type: ignore[typeddict-item]
execfile_('common.py', common_globals)  # type: ignore[name-defined]


MODEL = 'ST2030'
VERSION = '2.74'


class TechnicolorPlugin(common_globals['BaseTechnicolorPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True

    _COMMON_TEMPLATES = [('common/ST2030S.inf.tpl', 'ST2030S.inf')]
    _FILENAME_PREFIX = 'ST2030S'

    pg_associator = common_globals['BaseTechnicolorPgAssociator'](MODEL, VERSION)
