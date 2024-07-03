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
    'w53h': 'W53H-88.85.0.20.rom',
    'w56h': 'W56H-61.85.0.20.rom',
    'w57r': 'W57R-118.85.0.15.rom',
    'w59r': 'W59R-115.85.0.20.rom',
    'w73h': 'W73H-116.85.0.35.rom',
    'w74h': 'W74H-119.85.0.15.rom',
    'w78h': 'W78H-16.85.0.15.rom',
    'cp930w': 'CP930W-87.85.0.20.rom',
    't41s_dd10k': 'T4S-ddphone-66.85.0.56.rom',
    't54w_dd10k': 'T54W-ddphone-96.85.0.65.rom ',
}

MODEL_INFO = {
    'CP960': {
        'version': '73.85.0.5',
        'firmware': 'CP960-73.85.0.5.rom',
    },
    'CP920': {
        'version': '78.85.0.5',
        'firmware': 'CP920-78.85.0.5.rom',
    },
    'T27G': {
        'version': '69.85.0.5',
        'firmware': 'T27G-69.85.0.5.rom',
    },
    'T30': {
        'version': '124.85.0.40',
        'firmware': 'T31(T30,T30P,T31G,T31P,T33P,T33G)-124.85.0.40.rom',
    },
    'T30P': {
        'version': '124.85.0.40',
        'firmware': 'T31(T30,T30P,T31G,T31P,T33P,T33G)-124.85.0.40.rom',
    },
    'T31': {
        'version': '124.85.0.40',
        'firmware': 'T31(T30,T30P,T31G,T31P,T33P,T33G)-124.85.0.40.rom',
    },
    'T31P': {
        'version': '124.85.0.40',
        'firmware': 'T31(T30,T30P,T31G,T31P,T33P,T33G)-124.85.0.40.rom',
    },
    'T31G': {
        'version': '124.85.0.40',
        'firmware': 'T31(T30,T30P,T31G,T31P,T33P,T33G)-124.85.0.40.rom',
    },
    'T33P': {
        'version': '124.85.0.40',
        'firmware': 'T31(T30,T30P,T31G,T31P,T33P,T33G)-124.85.0.40.rom',
    },
    'T33G': {
        'version': '124.85.0.40',
        'firmware': 'T31(T30,T30P,T31G,T31P,T33P,T33G)-124.85.0.40.rom',
    },
    'T41S': {
        'version': '66.85.0.5',
        'firmware': 'T46S(T48S,T42S,T41S)-66.85.0.5.rom',
    },
    'T42S': {
        'version': '66.85.0.5',
        'firmware': 'T46S(T48S,T42S,T41S)-66.85.0.5.rom',
    },
    'T46S': {
        'version': '66.85.0.5',
        'firmware': 'T46S(T48S,T42S,T41S)-66.85.0.5.rom',
    },
    'T48S': {
        'version': '66.85.0.5',
        'firmware': 'T46S(T48S,T42S,T41S)-66.85.0.5.rom',
    },
    'T53': {
        'version': '96.85.0.5',
        'firmware': 'T54W(T57W,T53W,T53)-96.85.0.5.rom',
        'handsets_fw': HANDSETS_FW,
    },
    'T53W': {
        'version': '96.85.0.5',
        'firmware': 'T54W(T57W,T53W,T53)-96.85.0.5.rom',
        'handsets_fw': HANDSETS_FW,
    },
    'T54W': {
        'version': '96.85.0.5',
        'firmware': 'T54W(T57W,T53W,T53)-96.85.0.5.rom',
        'handsets_fw': HANDSETS_FW,
    },
    'T57W': {
        'version': '96.85.0.5',
        'firmware': 'T54W(T57W,T53W,T53)-96.85.0.5.rom',
        'handsets_fw': HANDSETS_FW,
    },
    'T58': {
        'version': '58.85.0.5',
        'firmware': 'T58-58.85.0.5.rom',
        'handsets_fw': HANDSETS_FW,
    },
    'W60B': {
        'version': '77.85.0.25',
        'firmware': 'W60B-77.85.0.25.rom',
        'handsets_fw': HANDSETS_FW,
    },
    'W70B': {
        'version': '146.85.0.37',
        'firmware': 'W70B-146.85.0.37.rom',
        'handsets_fw': HANDSETS_FW,
    },
    'W80DM': {
        'version': '103.85.0.25',
        'firmware': '$PN-103.85.0.25.rom',
        'handsets_fw': HANDSETS_FW,
    },
    'W80B': {
        'version': '103.85.0.25',
        'firmware': '$PN-103.85.0.25.rom',
        'handsets_fw': HANDSETS_FW,
    },
    'W90DM': {
        'version': '130.85.0.44',
        'firmware': '$PN-130.85.0.44.rom',  # $PN = Product Name, i.e W90DM
        'handsets_fw': HANDSETS_FW,
    },
    'W90B': {
        'version': '130.85.0.44',
        'firmware': '$PN-130.85.0.44.rom',  # $PN = Product Name, i.e W90B
        'handsets_fw': HANDSETS_FW,
    },
    'W75DM': {
        'version': '175.85.0.5',
        'firmware': 'W75DM-175.85.0.5.rom',
        'handsets_fw': HANDSETS_FW,
    },
    'W75B': {
        'version': '175.85.0.5',
        'firmware': 'W75DM-175.85.0.5.rom', # Yealink Inject W75B fw inside W75DM
        'handsets_fw': HANDSETS_FW,
    },
}


class YealinkPlugin(common_globals['BaseYealinkPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True

    pg_associator = common_globals['BaseYealinkPgAssociator'](MODEL_INFO)

    # Yealink plugin specific stuff

    _MODEL_INFO = MODEL_INFO
