# Copyright 2013-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

"""Plugin for Technicolor TB30 using the 1.74.0 SIP firmware."""
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


MODEL = 'TB30'
VERSION = '1.74.0'


class TechnicolorPlugin(common_globals['BaseTechnicolorPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True

    _COMMON_TEMPLATES = [('common/TB30S.inf.tpl', 'TB30S.inf')]
    _FILENAME_PREFIX = 'TB30S'

    pg_associator = common_globals['BaseTechnicolorPgAssociator'](MODEL, VERSION)
