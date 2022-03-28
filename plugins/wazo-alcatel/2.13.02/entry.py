# -*- coding: utf-8 -*-

# Copyright 2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

common = {}
execfile_('common.py', common)

MODELS_VERSIONS = {
    u'M3': u'2.13.02',
    u'M5': u'2.13.02',
    u'M7': u'2.13.02',
}


class AlcatelMyriadPlugin(common['BaseAlcatelPlugin']):
    IS_PLUGIN = True
    _MODELS_VERSIONS = MODELS_VERSIONS

    pg_associator = common['BaseAlcatelMyriadPgAssociator'](MODELS_VERSIONS)
