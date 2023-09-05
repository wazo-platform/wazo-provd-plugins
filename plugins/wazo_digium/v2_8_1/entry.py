# Copyright 2014-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypedDict
    from ..common.common import BaseDigiumPlugin, DigiumPgAssociator  # noqa: F401

    class CommonGlobalsDict(TypedDict):
        BaseDigiumPlugin: type[BaseDigiumPlugin]
        DigiumPgAssociator: type[DigiumPgAssociator]


common: CommonGlobalsDict = {}  # type: ignore[typeddict-item]
execfile_('common.py', common)  # type: ignore[name-defined]


VERSION = '2.8.1'


class DigiumPlugin(common['BaseDigiumPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True

    pg_associator = common['DigiumPgAssociator'](VERSION)
