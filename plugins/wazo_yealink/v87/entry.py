# Copyright 2013-2025 The Wazo Authors  (see the AUTHORS file)
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
    'w53h': 'W53H-88.85.0.20.rom',
    'w56h': 'W56H-61.85.0.20.rom',
    'w59r': 'W59R-115.85.0.20.rom',
    'cp930w': 'CP930W-87.85.0.20.rom',
    't41s_dd10k': 'T4S-ddphone-66.85.0.56.rom',
    't54w_dd10k': 'T54W-ddphone-96.85.0.65.rom ',
}

MODEL_INFO = {
    'T73U': {
        'version': '185.87.0.10',
        'firmware': 'T77(T73,T74,T73U,T74U,T77,T77U,T85W,T87W)-185.87.0.10.rom',
    },
    'T73W': {
        'version': '185.87.0.10',
        'firmware': 'T77(T73,T74,T73U,T74U,T77,T77U,T85W,T87W)-185.87.0.10.rom',
    },
    'T74U': {
        'version': '185.87.0.10',
        'firmware': 'T77(T73,T74,T73U,T74U,T77,T77U,T85W,T87W)-185.87.0.10.rom',
    },
    'T74W': {
        'version': '185.87.0.10',
        'firmware': 'T77(T73,T74,T73U,T74U,T77,T77U,T85W,T87W)-185.87.0.10.rom',
    },
    'T77U': {
        'version': '185.87.0.10',
        'firmware': 'T77(T73,T74,T73U,T74U,T77,T77U,T85W,T87W)-185.87.0.10.rom',
    },
    'T85W': {
        'version': '185.87.0.10',
        'firmware': 'T77(T73,T74,T73U,T74U,T77,T77U,T85W,T87W)-185.87.0.10.rom',
    },
    'T87W': {
        'version': '185.87.0.10',
        'firmware': 'T77(T73,T74,T73U,T74U,T77,T77U,T85W,T87W)-185.87.0.10.rom',
    },
    'T88W': {
        'version': '185.87.0.10',
        'firmware': 'T77(T73,T74,T73U,T74U,T77,T77U,T85W,T87W)-185.87.0.10.rom',
    },
    'T88V': {
        'version': '185.87.0.10',
        'firmware': 'T77(T73,T74,T73U,T74U,T77,T77U,T85W,T87W)-185.87.0.10.rom',
    },
    'AX83H': {
        'version': '180.87.0.5',
        'firmware': 'AX83(AX83,AX86)-180.87.0.5.rom',
    },
    'AX86R': {
        'version': '180.87.0.5',
        'firmware': 'AX83(AX83,AX86)-180.87.0.5.rom',
    },
}


class YealinkPlugin(common_globals['BaseYealinkPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True

    pg_associator = common_globals['BaseYealinkPgAssociator'](MODEL_INFO)

    # Yealink plugin specific stuff

    _MODEL_INFO = MODEL_INFO
