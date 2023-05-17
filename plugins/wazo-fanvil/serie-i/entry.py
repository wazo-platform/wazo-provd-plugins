# Copyright 2010-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


common = {}
execfile_('common.py', common)

MODELS = [
    'i10S',
    'i10SV',
    'i10SD',
    'i51W',
    'i52W',
    'i53W',
]

COMMON_FILES = {
    'F0V10S00000.cfg': (
        'i10S',
        'I10S-fanvil-3921-full-V0.2.2-2.12.19.9-1746-D0.29.0-T2023-04-14-09.42.06.z',
        'model-i10.tpl',
    ),
    'F0V10SV00000.cfg': (
        'i10SV',
        'I10SV-fanvil-3918-full-V0.2.2-2.12.19.9-1746-D0.29.0-T2023-04-14-09.42.06.z',
        'model-i10.tpl',
    ),
    'F0V10SD00000.cfg': (
        'i10SD',
        'I10SD-fanvil-3922-full-V0.2.2-2.12.19.9-1746-D0.29.0-T2023-04-14-09.42.06.z',
        'model-i10.tpl',
    ),
    'fanvil_i10s_hwv1_0.txt': (
        'i10S',
        'I10S-fanvil-3921-full-V0.2.2-2.12.19.9-1746-D0.29.0-T2023-04-14-09.42.06.z',
        'model-i10.tpl',
    ),
    'fanvil_i10sv_hwv1_0.txt': (
        'i10SV',
        'I10SV-fanvil-3918-full-V0.2.2-2.12.19.9-1746-D0.29.0-T2023-04-14-09.42.06.z',
        'model-i10.tpl',
    ),
    'fanvil_i10sd_hwv1_0.txt': (
        'i10SD',
        'I10SD-fanvil-3922-full-V0.2.2-2.12.19.9-1746-D0.29.0-T2023-04-14-09.42.06.z',
        'model-i10.tpl',
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
}

MODEL_FIRMWARE_MAPPING = {
    'i10S': 'I10S-fanvil-3921-full-V0.2.2-2.12.19.9-1746-D0.29.0-T2023-04-14-09.42.06.z',
    'i10SV': 'I10SV-fanvil-3918-full-V0.2.2-2.12.19.9-1746-D0.29.0-T2023-04-14-09.42.06.z',
    'i10SD': 'I10SD-fanvil-3922-full-V0.2.2-2.12.19.9-1746-D0.29.0-T2023-04-14-09.42.06.z',
    'i51W': 'i51w-fanvil-release-4900-2.12.9-krnvlT2022-09-06-10.31.48.z',
    'i52W': 'i52w-fanvil-release-4902-2.12.9-krnvlT2022-09-06-10.18.53.z',
    'i53W': 'i53w-fanvil-release-4908-2.12.9-krnvlT2022-09-06-09.59.22.z',
}

FUNCTION_KEYS_PER_PAGE = {
    'i10S': 1,
    'i10SV': 1,
    'i10SD': 2,
    'i51W': 3,
    'i52W': 3,
    'i53W': 3,
}


class FanvilPlugin(common['BaseFanvilPlugin']):
    IS_PLUGIN = True

    _COMMON_FILES = COMMON_FILES
    _MODELS = MODELS
    _MODEL_FIRMWARE_MAPPING = MODEL_FIRMWARE_MAPPING
    _FUNCTION_KEYS_PER_PAGE = FUNCTION_KEYS_PER_PAGE
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