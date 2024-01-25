# Copyright 2014-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

"""Plugin for Polycom phones using the 3.1.6.0017 SIP application.

The following Polycom phones are supported:
- SPIP301
- SPIP501
- SPIP600
- SPIP601
- SSIP4000

"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypedDict

    from ..common_v3.common import (  # noqa: F401
        BasePolycomPgAssociator,
        BasePolycomPlugin,
    )

    class CommonGlobalsDict(TypedDict):
        BasePolycomPlugin: type[BasePolycomPlugin]
        BasePolycomPgAssociator: type[BasePolycomPgAssociator]


common_globals: CommonGlobalsDict = {}  # type: ignore[typeddict-item]
execfile_('common.py', common_globals)  # type: ignore[name-defined]


MODELS = ['SPIP301', 'SPIP501', 'SPIP600', 'SPIP601', 'SSIP4000']
VERSION = '3.1.6.0017'


class PolycomPlugin(common_globals['BasePolycomPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True

    pg_associator = common_globals['BasePolycomPgAssociator'](MODELS, VERSION)
