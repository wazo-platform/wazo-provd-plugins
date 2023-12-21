# Copyright 2013-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypedDict

    from .common import BaseYealinkPgAssociator, BaseYealinkPlugin  # noqa: F401

    class CommonGlobalsDict(TypedDict):
        BaseYealinkPlugin: type[BaseYealinkPlugin]
        BaseYealinkPgAssociator: type[BaseYealinkPgAssociator]


common_globals: CommonGlobalsDict = {}  # type: ignore[typeddict-item]
execfile_('common.py', common_globals)  # type: ignore[name-defined]

HANDSETS_FW = {
    'w53h': 'W53H-88.83.0.90.rom',
    'w56h': 'W56H-61.83.0.90.rom',
    'w59r': 'W59R-115.83.0.10.rom',
    'cp930w': 'CP930W-87.83.0.60.rom',
}

MODEL_INFO = {
    'T19P_E2': {
        'version': '53.83.0.35',
        'firmware': 'T19P_E2-53.83.0.35.rom',
    },
    'T21P_E2': {
        'version': '52.83.0.35',
        'firmware': 'T21P_E2-52.83.0.35.rom',
    },
    'T23P': {
        'version': '44.83.0.35',
        'firmware': 'T23-44.83.0.35.rom',
    },
    'T23G': {
        'version': '44.83.0.35',
        'firmware': 'T23-44.83.0.35.rom',
    },
    'T27P': {
        'version': '45.83.0.35',
        'firmware': 'T27-45.83.0.35.rom',
    },
    'T27G': {
        'version': '69.83.0.35',
        'firmware': 'T27G-69.83.0.35.rom',
    },
    'T40P': {
        'version': '54.83.0.35',
        'firmware': 'T40-54.83.0.35.rom',
    },
    'T40G': {
        'version': '76.83.0.35',
        'firmware': 'T40G-76.83.0.35.rom',
    },
    'CP960': {
        'version': '73.83.0.30',
        'firmware': 'CP960-73.83.0.30.rom',
    },
    'T29G': {
        'version': '46.83.0.120',
        'firmware': 'T29-46.83.0.120.rom',
    },
    'T41P': {
        'version': '36.83.0.35',
        'firmware': 'T41-36.83.0.120.rom',
    },
    'T41S': {
        'version': '66.83.0.35',
        'firmware': 'T46S(T48S,T42S,T41S)-66.83.0.35.rom',
    },
    'T42S': {
        'version': '66.83.0.35',
        'firmware': 'T46S(T48S,T42S,T41S)-66.83.0.35.rom',
    },
    'T46S': {
        'version': '66.83.0.35',
        'firmware': 'T46S(T48S,T42S,T41S)-66.83.0.35.rom',
    },
    'T48S': {
        'version': '66.83.0.35',
        'firmware': 'T46S(T48S,T42S,T41S)-66.83.0.35.rom',
    },
    'T52S': {
        'version': '70.83.0.35',
        'firmware': 'T54S(T52S)-70.83.0.35.rom',
    },
    'T54S': {
        'version': '70.83.0.35',
        'firmware': 'T54S(T52S)-70.83.0.35.rom',
    },
    'T42G': {
        'version': '29.83.0.120',
        'firmware': 'T42-29.83.0.120.rom',
    },
    'T46G': {
        'version': '28.83.0.120',
        'firmware': 'T46-28.83.0.120.rom',
    },
    'T48G': {
        'version': '35.83.0.120',
        'firmware': 'T48-35.83.0.120.rom',
    },
    'T56A': {
        'version': '58.83.0.15',
        'firmware': 'T58V(T56A)-58.83.0.15.rom',
    },
    'T58': {
        'version': '58.83.0.15',
        'firmware': 'T58V(T56A)-58.83.0.15.rom',
    },
    'W60B': {
        'version': '77.83.0.85',
        'firmware': 'W60B-77.83.0.85.rom',
        'handsets_fw': HANDSETS_FW,
    },
    'W80B': {
        'version': '103.83.0.122',
        'firmware': '$PN-103.83.0.122.rom',  # $PN = Product Name, i.e W80B
        'handsets_fw': HANDSETS_FW,
    },
    'W80DM': {
        'version': '103.83.0.122',
        'firmware': '$PN-103.83.0.122.rom',  # $PN = Product Name, i.e W80B
        'handsets_fw': HANDSETS_FW,
    },
}


class YealinkPlugin(common_globals['BaseYealinkPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True

    pg_associator = common_globals['BaseYealinkPgAssociator'](MODEL_INFO)

    # Yealink plugin specific stuff

    _MODEL_INFO = MODEL_INFO
