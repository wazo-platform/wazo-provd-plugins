# Copyright 2013-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

"""Plugin for Avaya J100 series using the 04.01.03.06 SIP software."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypedDict

    from ..common.common import BaseAvayaPgAssociator, BaseAvayaPlugin  # noqa: F401

    class CommonGlobalsDict(TypedDict):
        BaseAvayaPlugin: type[BaseAvayaPlugin]
        BaseAvayaPgAssociator: type[BaseAvayaPgAssociator]


common_globals: CommonGlobalsDict = {}  # type: ignore[typeddict-item]
execfile_('common.py', common_globals)  # type: ignore[name-defined]


MODELS = ['J129', 'J139', 'J159', 'J169', 'J179', 'J189']
VERSION = '04.01.03.06'


class AvayaPlugin(common_globals['BaseAvayaPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True

    pg_associator = common_globals['BaseAvayaPgAssociator'](MODELS, VERSION)
