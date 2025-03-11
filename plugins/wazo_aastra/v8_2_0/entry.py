# Copyright 2015-2025 The Wazo Authors  (see the AUTHORS file)
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
    '6863i': '8.2.0',
    '6865i': '8.2.0',
    '6867i': '8.2.0',
    '6869i': '8.2.0',
    '6873i': '8.2.0',
    '6905': '8.2.0',
    '6910': '8.2.0',
    '6915': '8.2.0',
    '6920': '8.2.0',
    '6920w': '8.2.0',
    '6930': '8.2.0',
    '6930w': '8.2.0',
    '6940': '8.2.0',
    '6940w': '8.2.0',
    '6970': '8.2.0',
}


class AastraPlugin(common['BaseAastraPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True
    _LANGUAGE_PATH = 'Aastra/i18n/'

    pg_associator = common['BaseAastraPgAssociator'](MODEL_VERSIONS)
