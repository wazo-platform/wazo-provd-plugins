# Copyright 2020-2022 The Wazo Authors (see AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

common = {}
execfile_('common.py', common)

MODEL_VERSION = {
    'ATA191': 'MPP-11-1-0MPP0401-002',
    'ATA192': 'MPP-11-1-0MPP0401-002',
}


class CiscoSipPlugin(common['BaseCiscoSipPlugin']):
    IS_PLUGIN = True
    _COMMON_FILENAMES = [
        'ata191.cfg',
        'ata192.cfg',
    ]

    pg_associator = common['BaseCiscoPgAssociator'](MODEL_VERSION)
