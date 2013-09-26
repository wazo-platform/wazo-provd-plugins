# -*- coding: UTF-8 -*-

common_globals = {}
execfile_('common.py', common_globals)

MODELS = [
    u'SPIP321',
    u'SPIP331',
    u'SPIP335',
    u'SPIP450',
    u'SPIP550',
    u'SPIP560',
    u'SPIP650',
    u'SPIP670',
    u'SSIP5000',
    u'SSIP6000',
    u'SSIP7000',
]
VERSION = u'4.1.0.84959'


class PolycomPlugin(common_globals['BasePolycomPlugin']):
    IS_PLUGIN = True

    pg_associator = common_globals['BasePolycomPgAssociator'](MODELS, VERSION)
