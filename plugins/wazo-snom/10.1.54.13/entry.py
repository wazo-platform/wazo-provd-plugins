# Copyright 2018-2022 The Wazo Authors (see AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

common_globals = {}
execfile_('common.py', common_globals)

MODELS = [
    'D120',
    'D305',
    'D315',
    'D335',
    'D345',
    'D375',
    'D385',
    'D712',
    '715',
    'D717',
    '725',
    'D735',
    'D745',
    'D765',
    'D785',
]
VERSION = '10.1.54.13'


class SnomPlugin(common_globals['BaseSnomPlugin']):
    IS_PLUGIN = True

    _MODELS = MODELS

    pg_associator = common_globals['BaseSnomPgAssociator'](MODELS, VERSION)
