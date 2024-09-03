# Copyright 2013-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypedDict

    from ..common.common import BaseCiscoPgAssociator, BaseCiscoSccpPlugin  # noqa: F401

    class CommonGlobalsDict(TypedDict):
        BaseCiscoSccpPlugin: type[BaseCiscoSccpPlugin]
        BaseCiscoPgAssociator: type[BaseCiscoPgAssociator]


common: CommonGlobalsDict = {}  # type: ignore[typeddict-item]
execfile_('common.py', common)  # type: ignore[name-defined]

MODELS = [
    '7906G',
    '7911G',
    '7931G',
    '7941G',
    '7942G',
    '7945G',
    '7961G',
    '7962G',
    '7965G',
    '7970G',
    '7971G',
    '7975G',
]


class CiscoSccpPlugin(common['BaseCiscoSccpPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True

    pg_associator = common['BaseCiscoPgAssociator'](MODELS)
