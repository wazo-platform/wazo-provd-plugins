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

MODEL_VERSION = {
    'SPA901': '5.1.5',
    'SPA921': '5.1.8',
    'SPA922': '6.1.5(a)',
    'SPA941': '5.1.8',
    'SPA942': '6.1.5(a)',
    'SPA962': '6.1.5(a)',
}


class CiscoPlugin(common_globals['BaseCiscoPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True

    _ENCODING = 'ISO-8859-1'
    _COMMON_FILENAMES = [f'{model.lower()}.cfg' for model in MODEL_VERSION]

    pg_associator = common_globals['BaseCiscoPgAssociator'](MODEL_VERSION)
