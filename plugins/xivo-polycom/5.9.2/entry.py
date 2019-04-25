# -*- coding: utf-8 -*-

# Copyright 2018-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

common_globals = {}
execfile_('common.py', common_globals)

MODELS = [
    u'VVX101',
    u'VVX150',
    u'VVX201',
    u'VVX250',
    u'VVX300',
    u'VVX301',
    u'VVX310',
    u'VVX311',
    u'VVX350',
    u'VVX400',
    u'VVX401',
    u'VVX450',
    u'VVX410',
    u'VVX411',
    u'VVX500',
    u'VVX501',
    u'VVX600',
    u'VVX601',
    u'VVX1500',
]


class PolycomPlugin(common_globals['BasePolycomPlugin']):
    IS_PLUGIN = True

    pg_associator = common_globals['BasePolycomPgAssociator'](MODELS)
