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

MODEL_INFO = {
    'T19P_E2': {
        'version': '53.82.0.20',
        'firmware': 'T19P_E2-53.82.0.20.rom',
    },
    'T21P_E2': {
        'version': '52.82.0.20',
        'firmware': 'T21P_E2-52.82.0.20.rom',
    },
    'T23P': {
        'version': '44.82.0.20',
        'firmware': 'T23-44.82.0.20.rom',
    },
    'T23G': {
        'version': '44.82.0.20',
        'firmware': 'T23-44.82.0.20.rom',
    },
    'T27P': {
        'version': '45.82.0.30',
        'firmware': 'T27-45.82.0.30.rom',
    },
    'T27G': {
        'version': '69.82.0.30',
        'firmware': 'T27G-69.82.0.30.rom',
    },
    'T29G': {
        'version': '46.82.0.30',
        'firmware': 'T29-46.82.0.30.rom',
    },
    'T40P': {
        'version': '54.82.0.20',
        'firmware': 'T40-54.82.0.20.rom',
    },
    'T40G': {
        'version': '76.82.0.20',
        'firmware': 'T40G-76.82.0.20.rom',
    },
    'T41P': {
        'version': '36.82.0.20',
        'firmware': 'T41-36.82.0.20.rom',
    },
    'T41S': {
        'version': '66.82.0.30',
        'firmware': 'T46S(T48S,T42S,T41S)-66.82.0.30.rom',
    },
    'T42G': {
        'version': '29.82.0.20',
        'firmware': 'T42-29.82.0.20.rom',
    },
    'T42S': {
        'version': '66.82.0.30',
        'firmware': 'T46S(T48S,T42S,T41S)-66.82.0.30.rom',
    },
    'T46G': {
        'version': '28.82.0.30',
        'firmware': 'T46-28.82.0.30.rom',
    },
    'T46S': {
        'version': '66.82.0.30',
        'firmware': 'T46S(T48S,T42S,T41S)-66.82.0.30.rom',
    },
    'T48G': {
        'version': '35.82.0.30',
        'firmware': 'T48-35.82.0.30.rom',
    },
    'T48S': {
        'version': '66.82.0.30',
        'firmware': 'T46S(T48S,T42S,T41S)-66.82.0.30.rom',
    },
}


class YealinkPlugin(common_globals['BaseYealinkPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True

    pg_associator = common_globals['BaseYealinkPgAssociator'](MODEL_INFO)

    # Yealink plugin specific stuff

    _MODEL_INFO = MODEL_INFO
