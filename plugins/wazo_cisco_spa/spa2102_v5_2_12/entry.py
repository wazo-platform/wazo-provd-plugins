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
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypedDict
    from ..common.common import BaseCiscoPlugin, BaseCiscoPgAssociator  # noqa: F401

    class CommonGlobalsDict(TypedDict):
        BaseCiscoPlugin: type[BaseCiscoPlugin]
        BaseCiscoPgAssociator: type[BaseCiscoPgAssociator]


common_globals: CommonGlobalsDict = {}  # type: ignore[typeddict-item]
execfile_('common.py', common_globals)  # type: ignore[name-defined]

MODEL_VERSION = {'SPA2102': '5.2.12'}


class CiscoPlugin(common_globals['BaseCiscoPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True
    _COMMON_FILENAMES = ['spa2102.cfg']

    pg_associator = common_globals['BaseCiscoPgAssociator'](MODEL_VERSION)
