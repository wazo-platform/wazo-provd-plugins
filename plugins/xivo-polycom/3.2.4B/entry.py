# -*- coding: UTF-8 -*-

"""Plugin for Polycom phones using the 3.2.4.0267 SIP application.

The following Polycom phones are supported:
- SPIP320
- SPIP321
- SPIP330
- SPIP331
- SPIP335
- SPIP430
- SPIP450
- SPIP550
- SPIP560
- SPIP650
- SPIP670
- SSIP5000
- SSIP6000
- SSIP7000
- VVX1500

"""

# XXX version for VVX1500 is 3.2.4.0244, not 3.2.4.0267.

common_globals = {}
execfile_('common.py', common_globals)


MODELS = [u'SPIP320', u'SPIP321', u'SPIP330', u'SPIP331', u'SPIP335', u'SPIP430',
          u'SPIP450', u'SPIP550', u'SPIP560', u'SPIP650', u'SPIP670', u'SSIP5000',
          u'SSIP6000', u'SSIP7000', u'VVX1500']
VERSION = u'3.2.4.0267'


class PolycomPlugin(common_globals['BasePolycomPlugin']):
    IS_PLUGIN = True
    
    pg_associator = common_globals['BasePolycomPgAssociator'](MODELS, VERSION)
