# -*- coding: UTF-8 -*-

common_globals = {}
execfile_('common.py', common_globals)

MODELS = [
    u'VVX300',
    u'VVX310',
    u'VVX400',
    u'VVX410',
    u'VVX500',
    u'VVX600',
    u'VVX1500',
]
VERSION = u'5.0.0.6874'


class PolycomPlugin(common_globals['BasePolycomPlugin']):
    IS_PLUGIN = True

    pg_associator = common_globals['BasePolycomPgAssociator'](MODELS, VERSION)
