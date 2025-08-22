# Copyright 2017-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypedDict

    from ..common.common import BaseGigasetPgAssociator, BaseGigasetPlugin  # noqa: F401

    class CommonGlobalsDict(TypedDict):
        BaseGigasetPlugin: type[BaseGigasetPlugin]
        BaseGigasetPgAssociator: type[BaseGigasetPgAssociator]


common: CommonGlobalsDict = {}  # type: ignore[typeddict-item]
execfile_('common.py', common)  # type: ignore[name-defined]


MODEL_VERSIONS = {
    'N670 IP PRO': '83.V2.62.1',
    'N870 IP PRO': '83.V2.62.1',
    'N870E IP PRO': '83.V2.62.1',
}


class GigasetPlugin(common['BaseGigasetPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True

    pg_associator = common['BaseGigasetPgAssociator'](MODEL_VERSIONS)
