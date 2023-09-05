# Copyright 2020-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

common = {}
execfile_('common.py', common)

MODEL_VERSION = {
    '7811': '11.3.1',
    '7821': '11.3.1',
    '7832': '11.3.1',
    '7841': '11.3.1',
    '7861': '11.3.1',
    '6821': '11.3.1',
    '6841': '11.3.1',
    '6851': '11.3.1',
    '6861': '11.3.1',
    '6871': '11.3.1',
    '8811': '11.3.1',
    '8841': '11.3.1',
    '8851': '11.3.1',
    '8861': '11.3.1',
}


class CiscoSipPlugin(common['BaseCiscoSipPlugin']):
    IS_PLUGIN = True
    _COMMON_FILENAMES = [
        '7811-3PCC.xml',
        '7821-3PCC.xml',
        '7832-3PCC.xml',
        '7841-3PCC.xml',
        '7861-3PCC.xml',
        '6821-3PCC.xml',
        '6841-3PCC.xml',
        '6851-3PCC.xml',
        '6861-3PCC.xml',
        '6871-3PCC.xml',
        '8811-3PCC.xml',
        '8841-3PCC.xml',
        '8851-3PCC.xml',
        '8861-3PCC.xml',
    ]

    pg_associator = common['BaseCiscoPgAssociator'](MODEL_VERSION)
