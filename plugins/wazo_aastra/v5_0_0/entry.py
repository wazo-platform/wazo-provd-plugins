# Copyright 2015-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypedDict

    from ..common.common import BaseAastraPgAssociator, BaseAastraPlugin  # noqa: F401

    class CommonGlobalsDict(TypedDict):
        BaseAastraPlugin: type[BaseAastraPlugin]
        BaseAastraPgAssociator: type[BaseAastraPgAssociator]


common: CommonGlobalsDict = {}  # type: ignore[typeddict-item]
execfile_('common.py', common)  # type: ignore[name-defined]


MODEL_VERSIONS = {
    '6863i': '5.0.0.1018',
    '6865i': '5.0.0.1018',
    '6867i': '5.0.0.1018',
    '6869i': '5.0.0.1018',
    '6873i': '5.0.0.1018',
}


class AastraPlugin(common['BaseAastraPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True
    _LANGUAGE_PATH = 'Aastra/i18n/'

    pg_associator = common['BaseAastraPgAssociator'](MODEL_VERSIONS)
