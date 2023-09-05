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

"""Plugin for Alcatel phones using the SIP 2.01.10 firmware.

The following Alcatel "extended edition" phones are supported:
- 4008
- 4018

"""
from __future__ import annotations
from typing import TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from typing import TypedDict
    from .common import BaseAlcatelPlugin, BaseAlcatelPgAssociator  # noqa: F401

    class CommonGlobalsDict(TypedDict):
        BaseAlcatelPlugin: type[BaseAlcatelPlugin]
        BaseAlcatelPgAssociator: type[BaseAlcatelPgAssociator]


common_globals: CommonGlobalsDict = {}  # type: ignore[typeddict-item]
execfile_('common.py', common_globals)  # type: ignore[name-defined]

logger = logging.getLogger('plugin.wazo-alcatel')

MODELS = ['4008', '4018']
VERSION = '2.01.10'


class AlcatelPlugin(common_globals['BaseAlcatelPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True

    pg_associator = common_globals['BaseAlcatelPgAssociator'](MODELS, VERSION)
