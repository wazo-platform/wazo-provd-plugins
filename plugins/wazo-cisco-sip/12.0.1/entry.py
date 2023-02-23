# Copyright 2020-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

common = {}
execfile_('common.py', common)

MODEL_VERSION = {
    '8811': '12.0.1',
    '8841': '12.0.1',
    '8851': '12.0.1',
    '8861': '12.0.1',
}


class CiscoSipPlugin(common['BaseCiscoSipPlugin']):
    IS_PLUGIN = True
    _COMMON_FILENAMES = [
        '8811-3PCC.xml',
        '8841-3PCC.xml',
        '8851-3PCC.xml',
        '8861-3PCC.xml',
    ]

    pg_associator = common['BaseCiscoPgAssociator'](MODEL_VERSION)
