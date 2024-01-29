# Copyright 2013-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypedDict

    from ..common.common import (  # noqa: F401
        BaseTechnicolorPgAssociator,
        BaseTechnicolorPlugin,
    )

    class CommonGlobalsDict(TypedDict):
        BaseTechnicolorPlugin: type[BaseTechnicolorPlugin]
        BaseTechnicolorPgAssociator: type[BaseTechnicolorPgAssociator]


common_globals: CommonGlobalsDict = {}  # type: ignore[typeddict-item]
execfile_('common.py', common_globals)  # type: ignore[name-defined]

MODEL = 'ST2022'
VERSION = '4.78.1'


class TechnicolorPlugin(common_globals['BaseTechnicolorPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True

    _COMMON_TEMPLATES = [('common/ST2022S.inf.tpl', 'ST2022S.inf')]
    _FILENAME_PREFIX = 'ST2022S'
    _NB_FKEYS = 5
    _NB_LINES = 2

    pg_associator = common_globals['BaseTechnicolorPgAssociator'](MODEL, VERSION)
