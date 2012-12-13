# -*- coding: UTF-8 -*-

"""Plugin for Cisco SPA phones using the 7.5.2b firmware.

Warning you need to upgrade to this version before 7.5.4 !

The following Cisco phones are supported:
- SPA301
- SPA303
- SPA501G
- SPA502G
- SPA504G
- SPA508G
- SPA509G

The following Cisco expansion module are supported:
- SPA500S

"""

common_globals = {}
execfile_('common.py', common_globals)


PSN = [u'301', u'303', u'501G', u'502G', u'504G', u'508G', u'509G']
MODELS = [u'SPA' + psn for psn in PSN]
MODEL_VERSION = dict((model, u'7.5.2b') for model in MODELS)

class CiscoPlugin(common_globals['BaseCiscoPlugin']):
    IS_PLUGIN = True
    # similar to spa508G.cfg (G is uppercase)
    _COMMON_FILENAMES = ['spa' + psn.encode('ascii') + '.cfg' for psn in PSN]
    
    pg_associator = common_globals['BaseCiscoPgAssociator'](MODEL_VERSION)
