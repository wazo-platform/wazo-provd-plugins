# Copyright 2016-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

common = {}
execfile_('common.py', common)

MODELS = [
    'SN4112',
    'SN4112S',
    'SN4114',
    'SN4116',
    'SN4118',
    'SN4316',
    'SN4324',
    'SN4332',
]
VERSION = '6.11'


class PattonPlugin(common['BasePattonPlugin']):
    IS_PLUGIN = True

    pg_associator = common['BasePattonPgAssociator'](MODELS, VERSION)
