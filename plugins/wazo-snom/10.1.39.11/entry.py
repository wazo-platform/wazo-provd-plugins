# -*- coding: utf-8 -*-

# Copyright 2018-2020 The Wazo Authors (see AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

common_globals = {}
execfile_('common.py', common_globals)

MODELS = [
    u'D375',
    u'715',
    u'D717',
    u'725',
    u'D735',
    u'D745',
    u'D765',
    u'D785',
]
VERSION = u'10.1.39.11'


class SnomPlugin(common_globals['BaseSnomPlugin']):
    IS_PLUGIN = True

    _MODELS = MODELS

    pg_associator = common_globals['BaseSnomPgAssociator'](MODELS, VERSION)
