# -*- coding: UTF-8 -*-

common_globals = {}
execfile_('common.py', common_globals)

MODELS = [
    u'720',
]


class SnomPlugin(common_globals['BaseSnomPlugin']):
    IS_PLUGIN = True

    _MODELS = MODELS
