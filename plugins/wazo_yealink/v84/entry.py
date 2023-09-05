# Copyright 2013-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypedDict
    from .common import (  # noqa: F401
        BaseYealinkPlugin,
        BaseYealinkPgAssociator,
    )

    class CommonGlobalsDict(TypedDict):
        BaseYealinkPlugin: type[BaseYealinkPlugin]
        BaseYealinkPgAssociator: type[BaseYealinkPgAssociator]


common_globals: CommonGlobalsDict = {}  # type: ignore[typeddict-item]
execfile_('common.py', common_globals)  # type: ignore[name-defined]

MODEL_INFO = {
    'CP920': {
        'version': '78.84.0.125',
        'firmware': 'CP920-78.84.0.125.rom',
    },
    'CP960': {
        'version': '73.84.0.25',
        'firmware': 'CP960-73.84.0.25.rom',
    },
    'T19P_E2': {
        'version': '53.84.0.125',  # >=53.84.0.90 version does not support YDMP and YMCS
        'firmware': 'T19P_E2-53.84.0.125.rom',
    },
    'T21P_E2': {
        'version': '52.84.0.125',  # >=52.84.0.90 version does not support YDMP and YMCS
        'firmware': 'T21P_E2-52.84.0.125.rom',
    },
    'T23P': {
        'version': '44.84.0.140',  # >=44.84.0.90 version does not support YDMP and YMCS
        'firmware': 'T23-44.84.0.140.rom',
    },
    'T23G': {
        'version': '44.84.0.140',  # >=44.84.0.90 version does not support YDMP and YMCS
        'firmware': 'T23-44.84.0.140.rom',
    },
    'T27G': {
        'version': '69.84.0.125',
        'firmware': 'T27G-69.84.0.125.rom',
    },
    'T40P': {
        'version': '54.84.0.125',  # >=54.84.0.90 version does not support YDMP and YMCS
        'firmware': 'T40-54.84.0.125.rom',
    },
    'T40G': {
        'version': '76.84.0.125',  # >=76.84.0.90 version does not support YDMP and YMCS
        'firmware': 'T40G-76.84.0.125.rom',
    },
    'T41S': {
        'version': '66.84.0.125',
        'firmware': 'T46S(T48S,T42S,T41S)-66.84.0.125.rom',
    },
    'T42S': {
        'version': '66.84.0.125',
        'firmware': 'T46S(T48S,T42S,T41S)-66.84.0.125.rom',
    },
    'T46S': {
        'version': '66.84.0.125',
        'firmware': 'T46S(T48S,T42S,T41S)-66.84.0.125.rom',
    },
    'T48S': {
        'version': '66.84.0.125',
        'firmware': 'T46S(T48S,T42S,T41S)-66.84.0.125.rom',
    },
    'T52S': {
        'version': '70.84.0.70',
        'firmware': 'T54S(T52S)-70.84.0.70.rom',
    },
    'T53': {
        'version': '95.84.0.125',
        'firmware': 'T53W(T53)-95.84.0.125.rom',
    },
    'T53W': {
        'version': '95.84.0.125',
        'firmware': 'T53W(T53)-95.84.0.125.rom',
    },
    'T54S': {
        'version': '70.84.0.70',
        'firmware': 'T54S(T52S)-70.84.0.70.rom',
    },
    'T54W': {
        'version': '96.84.0.125',
        'firmware': 'T54W-96.84.0.125.rom',
    },
    'T57W': {
        'version': '97.84.0.125',
        'firmware': 'T57W-97.84.0.125.rom',
    },
    'T58': {
        'version': '58.84.0.25',
        'firmware': 'T58-58.84.0.25.rom',
    },
}


class YealinkPlugin(common_globals['BaseYealinkPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True

    pg_associator = common_globals['BaseYealinkPgAssociator'](MODEL_INFO)

    # Yealink plugin specific stuff

    _MODEL_INFO = MODEL_INFO
