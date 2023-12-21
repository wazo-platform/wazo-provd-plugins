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
    'w59r': 'W59R-115.85.0.20.rom',
    'cp930w': 'CP930W-87.85.0.20.rom',
    't41s_dd10k': 'T4S-ddphone-66.85.0.56.rom',
    't54w_dd10k': 'T54W-ddphone-96.85.0.65.rom ',
}

MODEL_INFO = {
    'CP920': {
        'version': '78.86.0.15',
        'firmware': 'CP920-78.86.0.15.rom',
    },
    'CP925': {
        'version': '148.86.0.5',
        'firmware': 'CP925-148.86.0.5.rom',
    },
    'T27G': {
        'version': '69.86.0.15',
        'firmware': 'T27G-69.86.0.15.rom',
    },
    'T30': {
        'version': '124.86.0.75',
        'firmware': 'T31(T30,T30P,T31G,T31P,T33P,T33G)-124.86.0.75.rom',
    },
    'T30P': {
        'version': '124.86.0.75',
        'firmware': 'T31(T30,T30P,T31G,T31P,T33P,T33G)-124.86.0.75.rom',
    },
    'T31': {
        'version': '124.86.0.75',
        'firmware': 'T31(T30,T30P,T31G,T31P,T33P,T33G)-124.86.0.75.rom',
    },
    'T31P': {
        'version': '124.86.0.75',
        'firmware': 'T31(T30,T30P,T31G,T31P,T33P,T33G)-124.86.0.75.rom',
    },
    'T31G': {
        'version': '124.86.0.75',
        'firmware': 'T31(T30,T30P,T31G,T31P,T33P,T33G)-124.86.0.75.rom',
    },
    'T31W': {
        'version': '124.86.0.75',
        'firmware': '',
        'handsets_fw': HANDSETS_FW,
    },
    'T33': {
        'version': '124.86.0.75',
        'firmware': 'T31(T30,T30P,T31G,T31P,T33P,T33G)-124.86.0.75.rom',
    },
    'T33P': {
        'version': '124.86.0.75',
        'firmware': 'T31(T30,T30P,T31G,T31P,T33P,T33G)-124.86.0.75.rom',
    },
    'T33G': {
        'version': '124.86.0.75',
        'firmware': 'T31(T30,T30P,T31G,T31P,T33P,T33G)-124.86.0.75.rom',
    },
    'T34W': {
        'version': '124.86.0.75',
        'firmware': '',
        'handsets_fw': HANDSETS_FW,
    },
    'T41S': {
        'version': '66.86.0.15',
        'firmware': 'T46S(T48S,T42S,T41S)-66.86.0.15.rom',
    },
    'T42S': {
        'version': '66.86.0.15',
        'firmware': 'T46S(T48S,T42S,T41S)-66.86.0.15.rom',
    },
    'T46S': {
        'version': '66.86.0.15',
        'firmware': 'T46S(T48S,T42S,T41S)-66.86.0.15.rom',
    },
    'T48S': {
        'version': '66.86.0.15',
        'firmware': 'T46S(T48S,T42S,T41S)-66.86.0.15.rom',
    },
    'T41U': {
        'version': '108.86.0.45',
        'firmware': 'T46U(T43U,T46U,T41U,T48U,T42U)-108.86.0.45(20211130).rom',
    },
    'T42U': {
        'version': '108.86.0.45',
        'firmware': 'T46U(T43U,T46U,T41U,T48U,T42U)-108.86.0.45(20211130).rom',
    },
    'T43U': {
        'version': '108.86.0.45',
        'firmware': 'T46U(T43U,T46U,T41U,T48U,T42U)-108.86.0.45(20211130).rom',
    },
    'T46U': {
        'version': '108.86.0.45',
        'firmware': 'T46U(T43U,T46U,T41U,T48U,T42U)-108.86.0.45(20211130).rom',
    },
    'T48U': {
        'version': '108.86.0.45',
        'firmware': 'T46U(T43U,T46U,T41U,T48U,T42U)-108.86.0.45(20211130).rom',
    },
    'T53': {
        'version': '96.86.0.45',
        'firmware': 'T54W(T57W,T53W,T53,T53C,T54,T57)-96.86.0.45(20211130).rom',
    },
    'T53C': {
        'version': '96.86.0.45',
        'firmware': 'T54W(T57W,T53W,T53,T53C,T54,T57)-96.86.0.45(20211130).rom',
    },
    'T53W': {
        'version': '96.86.0.45',
        'firmware': 'T54W(T57W,T53W,T53,T53C,T54,T57)-96.86.0.45(20211130).rom',
        'handsets_fw': HANDSETS_FW,
    },
    'T54W': {
        'version': '96.86.0.45',
        'firmware': 'T54W(T57W,T53W,T53,T53C,T54,T57)-96.86.0.45(20211130).rom',
        'handsets_fw': HANDSETS_FW,
    },
    'T57': {
        'version': '96.86.0.45',
        'firmware': 'T54W(T57W,T53W,T53,T53C,T54,T57)-96.86.0.45(20211130).rom',
    },
    'T57W': {
        'version': '96.86.0.45',
        'firmware': 'T54W(T57W,T53W,T53,T53C,T54,T57)-96.86.0.45(20211130).rom',
        'handsets_fw': HANDSETS_FW,
    },
    'T56': {
        'version': '58.86.0.20',
        'firmware': 'T58V(T56A)-58.86.0.20.rom',
    },
    'T58': {
        'version': '58.86.0.20',
        'firmware': 'T58V(T56A)-58.86.0.20.rom',
    },
    'T58W': {
        'version': '150.86.0.11',
        'firmware': 'T58W-150.86.0.11.rom',
        'handsets_fw': HANDSETS_FW,
    },
}


class YealinkPlugin(common_globals['BaseYealinkPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True

    pg_associator = common_globals['BaseYealinkPgAssociator'](MODEL_INFO)

    # Yealink plugin specific stuff

    _MODEL_INFO = MODEL_INFO
