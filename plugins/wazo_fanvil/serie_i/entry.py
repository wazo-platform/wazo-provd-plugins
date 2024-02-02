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
    'i10S',
    'i10SV',
    'i10SD',
    'i51W',
    'i52W',
    'i53W',
    'i16S',
    'i16SV',
    'i61',
    'i62',
    'i63',
    'i64',
]

COMMON_FILES = {
    'F0V10S00000.cfg': (
        'i10S',
        'I10S-fanvil-3921-full-V0.2.2-2.12.19.9-1746-D0.29.0-T2023-04-14-09.42.06.z',
        'model-i1x.tpl',
    ),
    'F0V10SV00000.cfg': (
        'i10SV',
        'I10SV-fanvil-3918-full-V0.2.2-2.12.19.9-1746-D0.29.0-T2023-04-14-09.42.06.z',
        'model-i1x.tpl',
    ),
    'F0V10SD00000.cfg': (
        'i10SD',
        'I10SD-fanvil-3922-full-V0.2.2-2.12.19.9-1746-D0.29.0-T2023-04-14-09.42.06.z',
        'model-i1x.tpl',
    ),
    'fanvil_i10s_hwv1_0.txt': (
        'i10S',
        'I10S-fanvil-3921-full-V0.2.2-2.12.19.9-1746-D0.29.0-T2023-04-14-09.42.06.z',
        'model-i1x.tpl',
    ),
    'fanvil_i10sv_hwv1_0.txt': (
        'i10SV',
        'I10SV-fanvil-3918-full-V0.2.2-2.12.19.9-1746-D0.29.0-T2023-04-14-09.42.06.z',
        'model-i1x.tpl',
    ),
    'fanvil_i10sd_hwv1_0.txt': (
        'i10SD',
        'I10SD-fanvil-3922-full-V0.2.2-2.12.19.9-1746-D0.29.0-T2023-04-14-09.42.06.z',
        'model-i1x.tpl',
    ),
    'F0Vi51W00000.cfg': (
        'i51W',
        'i51w-fanvil-release-4900-2.12.9-krnvlT2022-09-06-10.31.48.z',
        'model-i5x.tpl',
    ),
    'F0Vi52W00000.cfg': (
        'i52W',
        'i52w-fanvil-release-4902-2.12.9-krnvlT2022-09-06-10.18.53.z',
        'model-i5x.tpl',
    ),
    'F0Vi53W00000.cfg': (
        'i53W',
        'i53w-fanvil-release-4908-2.12.9-krnvlT2022-09-06-09.59.22.z',
        'model-i5x.tpl',
    ),
    'fanvil_i51w_hwv1_0.txt': (
        'i51w',
        'i51w-fanvil-release-4900-2.12.9-krnvlT2022-09-06-10.31.48.z',
        'model-i5x.tpl',
    ),
    'fanvil_i52w_hwv1_0.txt': (
        'i52w',
        'i52w-fanvil-release-4902-2.12.9-krnvlT2022-09-06-10.18.53.z',
        'model-i5x.tpl',
    ),
    'fanvil_i53w_hwv1_0.txt': (
        'i53w',
        'i53w-fanvil-release-4908-2.12.9-krnvlT2022-09-06-09.59.22.z',
        'model-i5x.tpl',
    ),
    'F0V16S00000.cfg': (
        'i16S',
        'I16S-fanvil-3925-full-V0.2.2-2.12.19.9-1746-D0.29.0-T2023-04-14-09.52.04.z',
        'model-i1x.tpl',
    ),
    'fanvil_i16s_hwv1_0.txt': (
        'i16S',
        'I16S-fanvil-3925-full-V0.2.2-2.12.19.9-1746-D0.29.0-T2023-04-14-09.52.04.z',
        'model-i1x.tpl',
    ),
    'F0V16SV00000.cfg': (
        'i16SV',
        'I16SV-fanvil-3919-full-V0.2.2-2.12.19.9-1746-D0.29.0-T2023-04-14-09.59.27.z',
        'model-i1x.tpl',
    ),
    'fanvil_i16sv_hwv1_0.txt': (
        'i16SV',
        'I16SV-fanvil-3919-full-V0.2.2-2.12.19.9-1746-D0.29.0-T2023-04-14-09.59.27.z',
        'model-i1x.tpl',
    ),
    'F0V0i6100000.cfg': (
        'i61',
        'I61-fanvil-3940-full-V0.2.2-2.12.19.9-1746-D0.29.0-T2023-04-14-10.13.47.z',
        'model-i6x.tpl',
    ),
    'fanvil_i61_hwv1_0.txt': (
        'i61',
        'I61-fanvil-3940-full-V0.2.2-2.12.19.9-1746-D0.29.0-T2023-04-14-10.13.47.z',
        'model-i6x.tpl',
    ),
    'F0V0i6200000.cfg': (
        'i62',
        'I62-fanvil-3941-full-V0.2.2-2.12.19.9-1746-D0.29.0-T2023-04-14-10.17.24.z',
        'model-i6x.tpl',
    ),
    'fanvil_i62_hwv1_0.txt': (
        'i62',
        'I62-fanvil-3941-full-V0.2.2-2.12.19.9-1746-D0.29.0-T2023-04-14-10.17.24.z',
        'model-i6x.tpl',
    ),
    'F0V0i6300000.cfg': (
        'i63',
        'I63-fanvil-3942-full-V0.2.2-2.12.19.9-1746-D0.29.0-T2023-04-14-10.20.57.z',
        'model-i6x.tpl',
    ),
    'fanvil_i63_hwv1_0.txt': (
        'i63',
        'I63-fanvil-3942-full-V0.2.2-2.12.19.9-1746-D0.29.0-T2023-04-14-10.20.57.z',
        'model-i6x.tpl',
    ),
    'F0V0i6400000.cfg': (
        'i64',
        'I64-fanvil-3943-full-V0.2.2-2.12.19.9-1746-D0.29.0-T2023-04-14-10.24.28.z',
        'model-i6x.tpl',
    ),
    'fanvil_i64_hwv1_0.txt': (
        'i64',
        'I64-fanvil-3943-full-V0.2.2-2.12.19.9-1746-D0.29.0-T2023-04-14-10.24.28.z',
        'model-i6x.tpl',
    ),
}

MODEL_FIRMWARE_MAPPING = {
    'i10S': 'I10S-fanvil-3921-full-V0.2.2-2.12.19.9-1746-D0.29.0-T2023-04-14-09.42.06.z',
    'i10SV': 'I10SV-fanvil-3918-full-V0.2.2-2.12.19.9-1746-D0.29.0-T2023-04-14-09.42.06.z',
    'i10SD': 'I10SD-fanvil-3922-full-V0.2.2-2.12.19.9-1746-D0.29.0-T2023-04-14-09.42.06.z',
    'i51W': 'i51w-fanvil-release-4900-2.12.9-krnvlT2022-09-06-10.31.48.z',
    'i52W': 'i52w-fanvil-release-4902-2.12.9-krnvlT2022-09-06-10.18.53.z',
    'i53W': 'i53w-fanvil-release-4908-2.12.9-krnvlT2022-09-06-09.59.22.z',
    'i16S': 'I16S-fanvil-3925-full-V0.2.2-2.12.19.9-1746-D0.29.0-T2023-04-14-09.52.04.z',
    'i16SV': 'I16SV-fanvil-3919-full-V0.2.2-2.12.19.9-1746-D0.29.0-T2023-04-14-09.59.27.z',
    'i61': 'I61-fanvil-3940-full-V0.2.2-2.12.19.9-1746-D0.29.0-T2023-04-14-10.13.47.z',
    'i62': 'I62-fanvil-3941-full-V0.2.2-2.12.19.9-1746-D0.29.0-T2023-04-14-10.17.24.z',
    'i63': 'I63-fanvil-3942-full-V0.2.2-2.12.19.9-1746-D0.29.0-T2023-04-14-10.20.57.z',
    'i64': 'I64-fanvil-3943-full-V0.2.2-2.12.19.9-1746-D0.29.0-T2023-04-14-10.24.28.z',
}

FUNCTION_KEYS_PER_PAGE = {
    'i10S': 1,
    'i10SV': 1,
    'i10SD': 2,
    'i51W': 3,
    'i52W': 3,
    'i53W': 3,
    'i16S': 1,
    'i16SV': 1,
    'i61': 1,
    'i62': 1,
    'i63': 5,
    'i64': 4,
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
