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
    'T19P_E2': {
        'version': '53.81.0.110',
        'firmware': 'T19P_E2-53.81.0.110.rom',
    },
    'T21P_E2': {
        'version': '52.81.0.110',
        'firmware': 'T21P_E2-52.81.0.110.rom',
    },
    'T23P': {
        'version': '44.81.0.110',
        'firmware': 'T23-44.81.0.110.rom',
    },
    'T23G': {
        'version': '44.81.0.110',
        'firmware': 'T23-44.81.0.110.rom',
    },
    'T27P': {
        'version': '45.81.0.110',
        'firmware': 'T27-45.81.0.110.rom',
    },
    'T27G': {
        'version': '69.81.0.110',
        'firmware': 'T27G-69.81.0.110.rom',
    },
    'T29G': {
        'version': '46.81.0.110',
        'firmware': 'T29-46.81.0.110.rom',
    },
    'T40P': {
        'version': '54.81.0.110',
        'firmware': 'T40-54.81.0.110.rom',
    },
    'T40G': {
        'version': '76.81.0.110',
        'firmware': 'T40G-76.81.0.110.rom',
    },
    'T41P': {
        'version': '36.81.0.110',
        'firmware': 'T41-36.81.0.110.rom',
    },
    'T41S': {
        'version': '66.81.0.110',
        'firmware': 'T41S-68.81.0.110.rom',
    },
    'T42G': {
        'version': '29.81.0.110',
        'firmware': 'T42-29.81.0.110.rom',
    },
    'T42S': {
        'version': '66.81.0.110',
        'firmware': 'T42S-67.81.0.110.rom',
    },
    'T46G': {
        'version': '28.81.0.110',
        'firmware': 'T46-28.81.0.110.rom',
    },
    'T46S': {
        'version': '66.81.0.110',
        'firmware': 'T46S-66.81.0.110.rom',
    },
    'T48G': {
        'version': '35.81.0.110',
        'firmware': 'T48-35.81.0.110.rom',
    },
    'T48S': {
        'version': '66.81.0.110',
        'firmware': 'T48S-65.81.0.110.rom',
    },
    'CP860': {
        'version': '37.81.0.10',
        'firmware': 'CP860-37.81.0.10.rom',
    },
    'CP920': {
        'version': '78.81.0.15',
        'firmware': 'CP920-78.81.0.15.rom',
    },
    'W52P': {
        'version': '25.81.0.60',
        'firmware': 'Base-W52P-W56P-25.81.0.60.rom',
        'handset_fw': 'W56H-61.81.0.30.rom',
    },
}


class YealinkPlugin(common_globals['BaseYealinkPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True

    pg_associator = common_globals['BaseYealinkPgAssociator'](MODEL_INFO)

    # Yealink plugin specific stuff

    _MODEL_INFO = MODEL_INFO
