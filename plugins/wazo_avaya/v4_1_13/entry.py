# Copyright 2013-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

"""Plugin for Avaya 1220IP and 1230IP using the 04.01.13.00 SIP software."""
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


MODELS = ['1220IP', '1230IP']
VERSION = '04.01.13.00'


class AvayaPlugin(common_globals['BaseAvayaPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True

    pg_associator = common_globals['BaseAvayaPgAssociator'](MODELS, VERSION)
