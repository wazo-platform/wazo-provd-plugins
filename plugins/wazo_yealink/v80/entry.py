# Copyright 2013-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypedDict
    from ..common.common import (  # noqa: F401
        BaseYealinkPlugin,
        BaseYealinkPgAssociator,
    )

    class CommonGlobalsDict(TypedDict):
        BaseYealinkPlugin: type[BaseYealinkPlugin]
        BaseYealinkPgAssociator: type[BaseYealinkPgAssociator]


common_globals: CommonGlobalsDict = {}  # type: ignore[typeddict-item]
execfile_('common.py', common_globals)  # type: ignore[name-defined]

MODEL_INFO = {
    'T19P_E2': {
        'version': '53.80.0.95',
        'firmware': 'T19P_E2-53.80.0.95.rom',
    },
    'T21P_E2': {
        'version': '52.80.0.95',
        'firmware': 'T21P_E2-52.80.0.95.rom',
    },
    'T23P': {
        'version': '44.80.0.95',
        'firmware': 'T23-44.80.0.95.rom',
    },
    'T23G': {
        'version': '44.80.0.95',
        'firmware': 'T23-44.80.0.95.rom',
    },
    'T27P': {
        'version': '45.80.0.95',
        'firmware': 'T27-45.80.0.95.rom',
    },
    'T29G': {
        'version': '46.80.0.95',
        'firmware': 'T29-46.80.0.95.rom',
    },
    'T40P': {
        'version': '54.80.0.95',
        'firmware': 'T40-54.80.0.95.rom',
    },
    'T41P': {
        'version': '36.80.0.95',
        'firmware': 'T41-36.80.0.95.rom',
    },
    'T42G': {
        'version': '29.80.0.95',
        'firmware': 'T42-29.80.0.95.rom',
    },
    'T46G': {
        'version': '28.80.0.95',
        'firmware': 'T46-28.80.0.95.rom',
    },
    'T48G': {
        'version': '35.80.0.95',
        'firmware': 'T48-35.80.0.95.rom',
    },
    'T49G': {
        'version': '51.80.0.100',
        'firmware': 'T49-51.80.0.100.rom',
    },
    'CP860': {
        'version': '37.80.0.30',
        'firmware': 'CP860-37.80.0.30.rom',
    },
    'CP960': {
        'version': '73.80.0.35',
        'firmware': 'CP960-73.80.0.35.rom',
    },
    'W52P': {
        'version': '25.80.0.15',
        'firmware': 'Base for W52P&W56P-25.80.0.15.rom',
        'handset_fw': 'W56H-61.80.0.15.rom',
    },
}


class YealinkPlugin(common_globals['BaseYealinkPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True

    pg_associator = common_globals['BaseYealinkPgAssociator'](MODEL_INFO)

    # Yealink plugin specific stuff

    _MODEL_INFO = MODEL_INFO
