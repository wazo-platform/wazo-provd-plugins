# Copyright 2013-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

common = {}
execfile_('common.py', common)

MODELS = [
    'GXP1100',
    'GXP1105',
    'GXP2100',
    'GXP2110',
    'GXP2120',
    'GXP2124',
]
VERSION = '1.0.8.6'


class GrandstreamPlugin(common['BaseGrandstreamPlugin']):
    IS_PLUGIN = True

    _MODELS = MODELS

    pg_associator = common['BaseGrandstreamPgAssociator'](MODELS, VERSION)
