# -*- coding: utf-8 -*-

# Copyright 2019 The Wazo Authors  (see AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

common_globals = {}
execfile_('common.py', common_globals)

MODELS = [
    '715',
    '725',
    'D120',
    'D305',
    'D315',
    'D345',
    'D375',
    'D385',
    'D712',
    'D717',
    'D735',
    'D745',
    'D765',
    'D785',

]
VERSION = '10.1.42.14'


class SnomPlugin(common_globals['BaseSnomPlugin']):
    IS_PLUGIN = True

    _MODELS = MODELS

    pg_associator = common_globals['BaseSnomPgAssociator'](MODELS, VERSION)
