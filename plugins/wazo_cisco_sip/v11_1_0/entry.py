# Copyright 2020-2023 The Wazo Authors  (see the AUTHORS file)
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
    'ATA191': 'MPP-11-1-0MPP0401-002',
    'ATA192': 'MPP-11-1-0MPP0401-002',
}


class CiscoSipPlugin(common['BaseCiscoSipPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True
    _COMMON_FILENAMES = [
        'ata191.cfg',
        'ata192.cfg',
    ]

    pg_associator = common['BaseCiscoPgAssociator'](MODEL_VERSION)
