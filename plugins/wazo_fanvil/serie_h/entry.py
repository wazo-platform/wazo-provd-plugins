# Copyright 2010-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypedDict

    from ..common.common import (  # noqa: F401
        BaseFanvilHTTPDeviceInfoExtractor,
        BaseFanvilPgAssociator,
        BaseFanvilPlugin,
    )

    class CommonGlobalsDict(TypedDict):
        BaseFanvilPlugin: type[BaseFanvilPlugin]
        BaseFanvilPgAssociator: type[BaseFanvilPgAssociator]
        BaseFanvilHTTPDeviceInfoExtractor: type[BaseFanvilHTTPDeviceInfoExtractor]


common: CommonGlobalsDict = {}  # type: ignore[typeddict-item]
execfile_('common.py', common)  # type: ignore[name-defined]

MODELS = [
    'H2U',
]

COMMON_FILES = {
    'F0V2UV200000.cfg': (
        'H2U',
        'h2u-v2-fanvil-release-ff01-5946-2.12.0-krnvUT2022-10-12-16.39.18.z',
        'model-h2x.tpl',
    ),
    'fanvil_h2u_v2_hwv1_0.txt': (
        'H2U',
        'h2u-v2-fanvil-release-ff01-5946-2.12.0-krnvUT2022-10-12-16.39.18.z',
        'model-h2x.tpl',
    ),
}

MODEL_FIRMWARE_MAPPING = {
    'H2U': 'h2u-v2-fanvil-release-ff01-5946-2.12.0-krnvUT2022-10-12-16.39.18.z',
}

FUNCTION_KEYS_PER_PAGE = {
    'H2U': 10,
}


class FanvilPlugin(common['BaseFanvilPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True

    _COMMON_FILES = COMMON_FILES
    _MODELS = MODELS
    _MODEL_FIRMWARE_MAPPING = MODEL_FIRMWARE_MAPPING
    _FUNCTION_KEYS_PER_PAGE = FUNCTION_KEYS_PER_PAGE
    _TOP_FUNCTION_KEYS: dict[str, int] = {}
    _LINE_KEYS_PER_PAGE: dict[str, int] = {}
    _LOCALE = {
        'de_DE': '16',
        'es_ES': '6',
        'fr_FR': '5',
        'fr_CA': '5',
        'it_IT': '7',
        'nl_NL': '3',
        'en_US': '0',
    }
    _TZ_INFO = {
        -12: [('UTC-12', -48)],
        -11: [('UTC-11', -44)],
        -10: [('UTC-10', -40)],
        -9: [('UTC-09', -36)],
        -8: [('UTC-08', -32)],
        -7: [('UTC-07', -28)],
        -6: [('UTC-06', -24)],
        -5: [('UTC-05', -20)],
        -4: [('UTC-04', -16)],
        -3: [('UTC-03', -12)],
        -2: [('UTC-02', -8)],
        -1: [('UTC-01', -4)],
        0: [('UCT', 0)],
        1: [('UTC+1', 4)],
        2: [('UTC+2', 8)],
        3: [('UTC+3', 12)],
        4: [('UTC+4', 16)],
        5: [('UTC+5', 20)],
        6: [('UTC+6', 24)],
        7: [('UTC+7', 28)],
        8: [('UTC+8', 32)],
        9: [('UTC+9', 36)],
        10: [('UTC+10', 40)],
        11: [('UTC+11', 44)],
        12: [('UTC+12', 48)],
    }

    pg_associator = common['BaseFanvilPgAssociator'](MODELS)
    http_dev_info_extractor = common['BaseFanvilHTTPDeviceInfoExtractor'](_COMMON_FILES)
