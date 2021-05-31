# -*- coding: utf-8 -*-

# Copyright 2013-2016 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

common = {}
execfile_('common.py', common)

MODELS = [
    u'GXP1100',
    u'GXP1105',
    u'GXP2100',
    u'GXP2110',
    u'GXP2120',
    u'GXP2124',
]
VERSION = u'1.0.8.6'


class GrandstreamPlugin(common['BaseGrandstreamPlugin']):
    IS_PLUGIN = True

    _MODELS = MODELS

    pg_associator = common['BaseGrandstreamPgAssociator'](MODELS, VERSION)
