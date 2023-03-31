# Copyright 2010-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


common = {}
execfile_('common.py', common)

MODELS = [
    'V67',
]

COMMON_FILES = {
    'F0V0V6700000.cfg': (
        'V67',
        'v67_fanvil_2.6.6.201_20230202_full.zip',
        'model-v.tpl',
    ),
    'fanvil_v67_hw1_1.txt': (
        'V67',
        'v67_fanvil_2.6.6.201_20230202_full.zip',
        'model-v67.tpl',
    ),
}

MODEL_FIRMWARE_MAPPING = {
    'V67': 'v67_fanvil_2.6.6.201_20230202_full.zip',
}

FUNCTION_KEYS_PER_PAGE = {
    'V67': 34,
}


class FanvilPlugin(common['BaseFanvilPlugin']):
    IS_PLUGIN = True

    _COMMON_FILES = COMMON_FILES
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
