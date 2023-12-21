# Copyright 2022-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypedDict

    from .common import BaseAlcatelMyriadPgAssociator, BaseAlcatelPlugin  # noqa: F401

    class CommonGlobalsDict(TypedDict):
        BaseAlcatelPlugin: type[BaseAlcatelPlugin]
        BaseAlcatelMyriadPgAssociator: type[BaseAlcatelMyriadPgAssociator]


common: CommonGlobalsDict = {}  # type: ignore[typeddict-item]
execfile_('common.py', common)  # type: ignore[name-defined]

MODELS_VERSIONS = {
    'M3': '2.13.02',
    'M5': '2.13.02',
    'M7': '2.13.02',
}


class AlcatelMyriadPlugin(common['BaseAlcatelPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True
    _MODELS_VERSIONS = MODELS_VERSIONS

    pg_associator = common['BaseAlcatelMyriadPgAssociator'](MODELS_VERSIONS)
