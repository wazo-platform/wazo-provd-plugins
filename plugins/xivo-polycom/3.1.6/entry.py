# -*- coding: UTF-8 -*-

"""Plugin for Polycom phones using the 3.1.6.0017 SIP application.

The following Polycom phones are supported:
- SPIP301
- SPIP501
- SPIP600
- SPIP601
- SSIP4000

"""

common_globals = {}
execfile_('common.py', common_globals)


MODELS = [u'SPIP301', u'SPIP501', u'SPIP600', u'SPIP601', u'SSIP4000']
VERSION = u'3.1.6.0017'


class PolycomPlugin(common_globals['BasePolycomPlugin']):
    IS_PLUGIN = True
    
    pg_associator = common_globals['BasePolycomPgAssociator'](MODELS, VERSION)
