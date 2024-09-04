# Copyright 2014-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypedDict

    from ..common.common import BaseCiscoPgAssociator, BaseCiscoPlugin  # noqa: F401

    class CommonGlobalsDict(TypedDict):
        BaseCiscoPlugin: type[BaseCiscoPlugin]
        BaseCiscoPgAssociator: type[BaseCiscoPgAssociator]


common_globals: CommonGlobalsDict = {}  # type: ignore[typeddict-item]
execfile_('common.py', common_globals)  # type: ignore[name-defined]

PSN = [
    '301',
    '303',
    '501G',
    '502G',
    '504G',
    '508G',
    '509G',
    '512G',
    '514G',
    '525G',
    '525G2',
]
MODELS = ['SPA' + psn for psn in PSN]
MODEL_VERSION = {model: '7.5.5' for model in MODELS}


class CiscoPlugin(common_globals['BaseCiscoPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True
    # similar to spa508G.cfg (G is uppercase)
    _COMMON_FILENAMES = [''.join(['spa', psn, '.cfg']) for psn in PSN]

    pg_associator = common_globals['BaseCiscoPgAssociator'](MODEL_VERSION)
