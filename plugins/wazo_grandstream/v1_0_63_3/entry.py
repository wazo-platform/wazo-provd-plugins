# Copyright 2021-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypedDict

    from ..common_ata.common import (  # noqa: F401
        BaseGrandstreamPgAssociator,
        BaseGrandstreamPlugin,
    )

    class CommonGlobalsDict(TypedDict):
        BaseGrandstreamPlugin: type[BaseGrandstreamPlugin]
        BaseGrandstreamPgAssociator: type[BaseGrandstreamPgAssociator]


common: CommonGlobalsDict = {}  # type: ignore[typeddict-item]
execfile_('common.py', common)  # type: ignore[name-defined]

MODELS = [
    'HT801',
    'HT802',
    'HT801V2',
    'HT802V2',
]
VERSION = [
    '1.0.63.3',
    '1.0.5.10',
]
MODEL_FIRMWARE_MAPPING = {
    'HT801': 'ht801fw.bin',
    'HT802': 'ht802fw.bin',
    'HT801V2': 'ht80xv2fw.bin',
    'HT802V2': 'ht80xv2fw.bin',
}


class GrandstreamPlugin(common['BaseGrandstreamPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True

    _MODELS = MODELS
    _MODEL_FIRMWARE_MAPPING = MODEL_FIRMWARE_MAPPING

    pg_associator = common['BaseGrandstreamPgAssociator'](MODELS, VERSION)
