# -*- coding: utf-8 -*-
# Copyright 2010-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

common = {}
execfile_('common.py', common)

MODELS = [
    u'X2',
    u'X210-Pro',
    u'X210i-Pro',
    u'X3',
    u'X3S',
    u'X4',
    u'X4U-Pro',
    u'X5',
    u'X5U-Pro',
    u'X5S',
    u'X6',
    u'X6V2',
    u'X6U-Pro',
    u'X7',
    u'X7-Pro',
    u'X7C',
    u'X7C-Pro',
]

COMMON_FILES = {
    'f0X2hw1.100.cfg': ('X2', u'x22.10.2.6887T20191115101133.z', 'model.tpl'),
    'F0V00X300000.cfg': ('X3', u'x31.4.0.2090T20180403152509.z', 'model.tpl'),
    'f0X3shw1.100.cfg': ('X3S', u'x3s2.10.2.6887T20191115101938.z', 'model.tpl'),
    'f0X4hw1.100.cfg': ('X4', u'x42.10.2.6887T20191122095252.z', 'model.tpl'),
    'f0X5hw1.100.cfg': ('X5', u'x51.4.0.2016T20170303151233.z', 'model.tpl'),
    'F0V00X5S0000.cfg': ('X5S', u'x5s-6900-P0.16.5-1.12.2-3144T2019-07-23-14.20.37.z', 'model.tpl'),
    'F0V00X600000.cfg': ('X6', u'x6-6904-P0.16.5-1.12.2-3144T2019-07-29-15.09.59.z', 'model.tpl'),
    'F0000X600000.cfg': ('X6V2', u'x6-6914-P0.16.5-1.12.2-3144T2019-07-23-14.20.41.z', 'model.tpl'),
}

MODEL_FIRMWARE_MAPPING = {
    u'X210-Pro': u'x210pro-fanvil-release-6959-2.12.1.3-krnvlT2022-05-14-17.24.15.z',
    u'X210i-Pro': u'x210ipro-fanvil-release-6960-2.12.1.3-krnvlT2022-05-14-17.29.43.z',
    u'X4U-Pro': u'x4upro-fanvil-release-ff01-6903-2.12.4.1-krnvUT2022-05-18-17.16.07.z',
    u'X5U-Pro': u'x5upro-fanvil-release-ff01-6907-2.12.4.1-krnvUT2022-05-18-17.22.39.z',
    u'X6U-Pro': u'x6upro-fanvil-release-ff01-6916-2.12.4.1-krnvUT2022-05-18-17.47.06.z',
    u'X7': u'x7-6926-P0.17.0-1.12.5.1-3739T2019-11-07-18.19.52.z',
    u'X7-Pro': u'x7upro-fanvil-release-6957-2.12.1.3-krnvlT2022-05-14-17.01.35.z',
    u'X7C': u'x7c-6925-P0.17.0-1.12.2.1-3739T2019-11-07-18.27.06.z',
    u'X7C-Pro': u'x7upro-fanvil-release-6957-2.12.1.3-krnvlT2022-05-14-17.01.35.z',
}


class FanvilPlugin(common['BaseFanvilPlugin']):
    IS_PLUGIN = True

    _COMMON_FILES = COMMON_FILES
    _MODEL_FIRMWARE_MAPPING = MODEL_FIRMWARE_MAPPING
    _LOCALE = {
        u'de_DE': '16',
        u'es_ES': '10',
        u'fr_FR': '4',
        u'fr_CA': '4',
        u'it_IT': '7',
        u'nl_NL': '3',
        u'en_US': '0'
    }
    _TZ_INFO = {
        -12: [(u'UTC-12', -48)],
        -11: [(u'UTC-11', -44)],
        -10: [(u'UTC-10', -40)],
        -9: [(u'UTC-09', -36)],
        -8: [(u'UTC-08', -32)],
        -7: [(u'UTC-07', -28)],
        -6: [(u'UTC-06', -24)],
        -5: [(u'UTC-05', -20)],
        -4: [(u'UTC-04', -16)],
        -3: [(u'UTC-03', -12)],
        -2: [(u'UTC-02', -8)],
        -1: [(u'UTC-01', -4)],
        0: [(u'UCT', 0)],
        1: [(u'UTC+1', 4)],
        2: [(u'UTC+2', 8)],
        3: [(u'UTC+3', 12)],
        4: [(u'UTC+4', 16)],
        5: [(u'UTC+5', 20)],
        6: [(u'UTC+6', 24)],
        7: [(u'UTC+7', 28)],
        8: [(u'UTC+8', 32)],
        9: [(u'UTC+9', 36)],
        10: [(u'UTC+10', 40)],
        11: [(u'UTC+11', 44)],
        12: [(u'UTC+12', 48)],
    }

    pg_associator = common['BaseFanvilPgAssociator'](MODELS)
    http_dev_info_extractor = common['BaseFanvilHTTPDeviceInfoExtractor'](_COMMON_FILES)
