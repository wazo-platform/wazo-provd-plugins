# Copyright 2016-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypedDict

    from ..common.common import BasePattonPgAssociator, BasePattonPlugin  # noqa: F401

    class CommonGlobalsDict(TypedDict):
        BasePattonPlugin: type[BasePattonPlugin]
        BasePattonPgAssociator: type[BasePattonPgAssociator]


common: CommonGlobalsDict = {}  # type: ignore[typeddict-item]
execfile_('common.py', common)  # type: ignore[name-defined]

MODELS = [
    'SN4112',
    'SN4112S',
    'SN4114',
    'SN4116',
    'SN4118',
    'SN4316',
    'SN4324',
    'SN4332',
]
VERSION = '6.9'


class PattonPlugin(common['BasePattonPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True

    pg_associator = common['BasePattonPgAssociator'](MODELS, VERSION)
