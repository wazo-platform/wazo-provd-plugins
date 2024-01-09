# Copyright 2013-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypedDict

    from ..common.common import BaseYealinkPgAssociator, BaseYealinkPlugin  # noqa: F401

    class CommonGlobalsDict(TypedDict):
        BaseYealinkPlugin: type[BaseYealinkPlugin]
        BaseYealinkPgAssociator: type[BaseYealinkPgAssociator]


common_globals: CommonGlobalsDict = {}  # type: ignore[typeddict-item]
execfile_('common.py', common_globals)  # type: ignore[name-defined]


MODEL_INFO = {
    'T20P': {
        'version': '9.73.0.50',
        'firmware': '9.73.0.50.rom',
    },
    'T22P': {
        'version': '7.73.0.50',
        'firmware': '7.73.0.50.rom',
    },
    'T26P': {
        'version': '6.73.0.50',
        'firmware': '6.73.0.50.rom',
    },
    'T28P': {
        'version': '2.73.0.50',
        'firmware': '2.73.0.50.rom',
    },
    'W52P': {
        'version': '25.73.0.40',
        'firmware': '25.73.0.40.rom',
        'handset_fw': '26.73.0.30.rom',
    },
}


class YealinkPlugin(common_globals['BaseYealinkPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True

    pg_associator = common_globals['BaseYealinkPgAssociator'](MODEL_INFO)

    # Yealink plugin specific stuff

    _MODEL_INFO = MODEL_INFO
