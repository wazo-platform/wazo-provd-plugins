# Copyright 2020-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypedDict

    from .common import BaseCiscoPgAssociator, BaseCiscoSipPlugin  # noqa: F401

    class CommonGlobalsDict(TypedDict):
        BaseCiscoSipPlugin: type[BaseCiscoSipPlugin]
        BaseCiscoPgAssociator: type[BaseCiscoPgAssociator]


common: CommonGlobalsDict = {}  # type: ignore[typeddict-item]
execfile_('common.py', common)  # type: ignore[name-defined]

MODEL_VERSION = {
    # 78xx
    '7811': '12.0.7',
    '7821': '12.0.7',
    '7832': '12.0.7',
    '7841': '12.0.7',
    '7861': '12.0.7',
    # 88xx
    '8811': '12.0.7',
    '8841': '12.0.7',
    '8851': '12.0.7',
    '8861': '12.0.7',
}


class CiscoSipPlugin(common['BaseCiscoSipPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True
    _COMMON_FILENAMES = [
        '7811-3PCC.xml',
        '7821-3PCC.xml',
        '7832-3PCC.xml',
        '7841-3PCC.xml',
        '7861-3PCC.xml',
        '8811-3PCC.xml',
        '8841-3PCC.xml',
        '8851-3PCC.xml',
        '8861-3PCC.xml',
    ]

    pg_associator = common['BaseCiscoPgAssociator'](MODEL_VERSION)
