# Copyright 2021-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypedDict

    from ..common_dect.common import BaseSnomPgAssociator, BaseSnomPlugin  # noqa: F401

    class CommonGlobalsDict(TypedDict):
        BaseSnomPlugin: type[BaseSnomPlugin]
        BaseSnomPgAssociator: type[BaseSnomPgAssociator]


common_globals: CommonGlobalsDict = {}  # type: ignore[typeddict-item]
execfile_('common.py', common_globals)  # type: ignore[name-defined]

MODELS = [
    'M400',
    'M900',
]
VERSION = '07.40.0104'


class SnomPlugin(common_globals['BaseSnomPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True

    _MODELS = MODELS

    pg_associator = common_globals['BaseSnomPgAssociator'](MODELS, VERSION)
