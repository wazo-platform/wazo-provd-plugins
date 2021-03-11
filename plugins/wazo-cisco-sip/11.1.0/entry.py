# -*- coding: utf-8 -*-

# Copyright 2020 The Wazo Authors (see AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

common = {}
execfile_('common.py', common)

MODEL_VERSION = {
    u'ATA191': u'MPP-11-1-0MPP0401-002',
    u'ATA192': u'MPP-11-1-0MPP0401-002',
}


class CiscoSipPlugin(common['BaseCiscoSipPlugin']):
    IS_PLUGIN = True
    _COMMON_FILENAMES = [
        u'ata191.cfg',
        u'ata192.cfg',
    ]

    pg_associator = common['BaseCiscoPgAssociator'](MODEL_VERSION)
