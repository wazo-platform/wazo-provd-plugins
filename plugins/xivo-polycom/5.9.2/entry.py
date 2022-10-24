# Copyright 2018-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

common_globals = {}
execfile_('common.py', common_globals)

MODELS = [
    'VVX101',
    'VVX150',
    'VVX201',
    'VVX250',
    'VVX300',
    'VVX301',
    'VVX310',
    'VVX311',
    'VVX350',
    'VVX400',
    'VVX401',
    'VVX450',
    'VVX410',
    'VVX411',
    'VVX500',
    'VVX501',
    'VVX600',
    'VVX601',
    'VVX1500',
]


class PolycomPlugin(common_globals['BasePolycomPlugin']):
    IS_PLUGIN = True

    pg_associator = common_globals['BasePolycomPgAssociator'](MODELS)
