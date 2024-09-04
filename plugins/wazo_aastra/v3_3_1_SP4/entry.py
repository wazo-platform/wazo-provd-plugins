# Copyright 2014-2024 The Wazo Authors  (see the AUTHORS file)
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
    '6730i': '3.3.1.4365',
    '6731i': '3.3.1.4365',
    '6735i': '3.3.1.8215',
    '6737i': '3.3.1.8215',
    '6739i': '3.3.1.4365',
    '6753i': '3.3.1.4365',
    '6755i': '3.3.1.4365',
    '6757i': '3.3.1.4365',
    '9143i': '3.3.1.4365',
    '9480i': '3.3.1.4365',
}


class AastraPlugin(common['BaseAastraPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True
    _LANGUAGE_PATH = 'i18n/'

    pg_associator = common['BaseAastraPgAssociator'](MODEL_VERSIONS)
