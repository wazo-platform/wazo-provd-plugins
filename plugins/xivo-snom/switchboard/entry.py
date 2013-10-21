# -*- coding: UTF-8 -*-

common_globals = {}
execfile_('common.py', common_globals)

MODELS = [
    u'720',
]
VERSION = u'8.7.3.19'


class SnomPlugin(common_globals['BaseSnomPlugin']):
    IS_PLUGIN = True

    _MODELS = MODELS

    pg_associator = common_globals['BaseSnomPgAssociator'](MODELS, VERSION)
