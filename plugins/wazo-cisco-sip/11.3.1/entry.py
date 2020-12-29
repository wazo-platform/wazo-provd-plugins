# -*- coding: utf-8 -*-

# Copyright 2020 The Wazo Authors (see AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

common = {}
execfile_('common.py', common)

MODEL_VERSION = {
    u'7811': u'11.3.1',
    u'7821': u'11.3.1',
    u'7832': u'11.3.1',
    u'7841': u'11.3.1',
    u'7861': u'11.3.1',
    u'6821': u'11.3.1',
    u'6841': u'11.3.1',
    u'6851': u'11.3.1',
    u'6861': u'11.3.1',
    u'6871': u'11.3.1',
}


class CiscoSipPlugin(common['BaseCiscoSipPlugin']):
    IS_PLUGIN = True
    _COMMON_FILENAMES = [
        u'7811-3PCC.xml',
        u'7821-3PCC.xml',
        u'7832-3PCC.xml',
        u'7841-3PCC.xml',
        u'7861-3PCC.xml',
        u'6821-3PCC.xml',
        u'6841-3PCC.xml',
        u'6851-3PCC.xml',
        u'6861-3PCC.xml',
        u'6871-3PCC.xml',
    ]

    pg_associator = common['BaseCiscoPgAssociator'](MODEL_VERSION)
