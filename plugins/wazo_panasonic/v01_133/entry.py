# Copyright 2013-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypedDict

    from ..common.common import (  # noqa: F401
        BasePanasonicPgAssociator,
        BasePanasonicPlugin,
    )

    class CommonGlobalsDict(TypedDict):
        BasePanasonicPlugin: type[BasePanasonicPlugin]
        BasePanasonicPgAssociator: type[BasePanasonicPgAssociator]


common: CommonGlobalsDict = {}  # type: ignore[typeddict-item]
execfile_('common.py', common)  # type: ignore[name-defined]

logger = logging.getLogger('plugin.wazo-panasonic')


MODELS = ['KX-UT113', 'KX-UT123', 'KX-UT133', 'KX-UT136']
VERSION = '01.133'


class PanasonicPlugin(common['BasePanasonicPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True

    _MODELS = MODELS

    pg_associator = common['BasePanasonicPgAssociator'](MODELS, VERSION)
