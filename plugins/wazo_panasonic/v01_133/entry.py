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
from __future__ import annotations
from typing import TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from typing import TypedDict
    from ..common.common import (  # noqa: F401
        BasePanasonicPlugin,
        BasePanasonicPgAssociator,
    )

    class CommonGlobalsDict(TypedDict):
        BasePanasonicPlugin: type[BasePanasonicPlugin]
        BasePanasonicPgAssociator: type[BasePanasonicPgAssociator]


common: CommonGlobalsDict = {}  # type: ignore[typeddict-item]
execfile_('common.py', common)  # type: ignore[name-defined]

logger = logging.getLogger('plugin.wazo-panasonic')


MODELS = ['KX-UT113', 'KX-UT123', 'KX-UT133', 'KX-UT136']
VERSION = '01.133'


class PanasonicPlugin(common['BasePanasonicPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True

    _MODELS = MODELS

    pg_associator = common['BasePanasonicPgAssociator'](MODELS, VERSION)
