# Copyright 2010-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


common = {}
execfile_('common.py', common)

MODELS = [
    'X2',
    'X210',
    'X210i',
    'X210-Pro',
    'X210i-Pro',
    'X3',
    'X3S',
    'X4',
    'X4U',
    'X4U-Pro',
    'X5',
    'X5U',
    'X5U-Pro',
    'X5S',
    'X6',
    'X6V2',
    'X6U',
    'X6U-Pro',
    'X7',
    'X7-Pro',
    'X7C',
    'X7C-Pro',
]

COMMON_FILES = {
    'f0X2hw1.100.cfg': ('X2', 'x22.10.2.6887T20191115101133.z', 'model.tpl'),
    'F0V00X300000.cfg': ('X3', 'x31.4.0.2090T20180403152509.z', 'model.tpl'),
    'f0X3shw1.100.cfg': ('X3S', 'x3s2.10.2.6887T20191115101938.z', 'model.tpl'),
    'f0X4hw1.100.cfg': ('X4', 'x42.10.2.6887T20191122095252.z', 'model.tpl'),
    'f0X5hw1.100.cfg': ('X5', 'x51.4.0.2016T20170303151233.z', 'model.tpl'),
    'F0V00X5S0000.cfg': (
        'X5S',
        'x5s-6900-P0.16.5-1.12.2-3144T2019-07-23-14.20.37.z',
        'model.tpl',
    ),
    'F0V00X600000.cfg': (
        'X6',
        'x6-6904-P0.16.5-1.12.2-3144T2019-07-29-15.09.59.z',
        'model.tpl',
    ),
    'F0000X600000.cfg': (
        'X6V2',
        'x6-6914-P0.16.5-1.12.2-3144T2019-07-23-14.20.41.z',
        'model.tpl',
    ),
}

MODEL_FIRMWARE_MAPPING = {
    'X210': 'x210-6924-P0.18.23.89-2.4.5.2-3594T2022-07-29-09.44.03.z',
    'X210-Pro': 'x210pro-fanvil-release-6959-2.12.1.3-krnvlT2022-05-14-17.24.15.z',
    'X210i': 'x210i-6923-P0.18.23.89-2.4.5.2-3594T2022-07-29-09.53.39.z',
    'X210i-Pro': 'x210ipro-fanvil-release-6960-2.12.1.3-krnvlT2022-05-14-17.29.43.z',
    'X4U': 'x4u-6902-P0.18.23.89-2.4.5.2-3594T2022-07-29-09.39.20.z',
    'X4U-Pro': 'x4upro-fanvil-release-ff01-6903-2.12.4.1-krnvUT2022-05-18-17.16.07.z',
    'X5U': 'x5u-6906-P0.18.23.89-2.4.5.2-3594T2022-07-29-09.20.52.z',
    'X5U-Pro': 'x5upro-fanvil-release-ff01-6907-2.12.4.1-krnvUT2022-05-18-17.22.39.z',
    'X6U': 'x6u-6915-P0.18.23.89-2.4.5.2-3594T2022-07-28-17.32.21.z',
    'X6U-Pro': 'x6upro-fanvil-release-ff01-6916-2.12.4.1-krnvUT2022-05-18-17.47.06.z',
    'X7': 'x7-6926-P0.18.23.89-2.4.5.2-4229T2022-07-29-16.11.47.z',
    'X7-Pro': 'x7upro-fanvil-release-6957-2.12.1.3-krnvlT2022-05-14-17.01.35.z',
    'X7C': 'x7c-6925-P0.18.23.89-2.4.5.2-4229T2022-07-29-16.16.20.z',
    'X7C-Pro': 'x7upro-fanvil-release-6957-2.12.1.3-krnvlT2022-05-14-17.01.35.z',
}

FUNCTION_KEYS_PER_PAGE = {
    'X210': 32,
    'X210i': 32,
    'X4U': 6,
    'X5U': 6,
    'X6U': 12,
}


class FanvilPlugin(common['BaseFanvilPlugin']):
    IS_PLUGIN = True

    _COMMON_FILES = COMMON_FILES
    _MODEL_FIRMWARE_MAPPING = MODEL_FIRMWARE_MAPPING
    _FUNCTION_KEYS_PER_PAGE = FUNCTION_KEYS_PER_PAGE
    _LOCALE = {
        'de_DE': '16',
        'es_ES': '10',
        'fr_FR': '4',
        'fr_CA': '4',
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
