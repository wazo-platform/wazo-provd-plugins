# Copyright 2020-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypedDict
    from .common import BaseCiscoSipPlugin, BaseCiscoPgAssociator  # noqa: F401

    class CommonGlobalsDict(TypedDict):
        BaseCiscoSipPlugin: type[BaseCiscoSipPlugin]
        BaseCiscoPgAssociator: type[BaseCiscoPgAssociator]


common: CommonGlobalsDict = {}  # type: ignore[typeddict-item]
execfile_('common.py', common)  # type: ignore[name-defined]

MODEL_VERSION = {
    '8811': '12.0.1',
    '8841': '12.0.1',
    '8851': '12.0.1',
    '8861': '12.0.1',
}


class CiscoSipPlugin(common['BaseCiscoSipPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True
    _COMMON_FILENAMES = [
        '8811-3PCC.xml',
        '8841-3PCC.xml',
        '8851-3PCC.xml',
        '8861-3PCC.xml',
    ]

    pg_associator = common['BaseCiscoPgAssociator'](MODEL_VERSION)
