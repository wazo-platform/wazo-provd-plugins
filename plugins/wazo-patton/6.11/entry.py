# -*- coding: utf-8 -*-

# Copyright 2016-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

common = {}
execfile_('common.py', common)

MODELS = [
    u'SN4112',
    u'SN4112S',
    u'SN4114',
    u'SN4116',
    u'SN4118',
    u'SN4316',
    u'SN4324',
    u'SN4332',
]
VERSION = u'6.11'


class PattonPlugin(common['BasePattonPlugin']):
    IS_PLUGIN = True

    pg_associator = common['BasePattonPgAssociator'](MODELS, VERSION)
