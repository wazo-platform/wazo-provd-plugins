# Copyright 2013-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

"""Plugin for Zenitel IP stations using the 01.11.3.2 firmware.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypedDict

    from ..common.common import BaseZenitelPlugin  # noqa: F401

    class CommonGlobalsDict(TypedDict):
        BaseZenitelPlugin: type[BaseZenitelPlugin]


common_globals: CommonGlobalsDict = {}  # type: ignore[typeddict-item]
execfile_('common.py', common_globals)  # type: ignore[name-defined]


class ZenitelPlugin(common_globals['BaseZenitelPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True
