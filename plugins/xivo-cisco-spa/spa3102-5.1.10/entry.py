# -*- coding: UTF-8 -*-

"""Plugin for Cisco SPA3102 in version 5.1.10."""

common_globals = {}
execfile_('common.py', common_globals)


MODEL_VERSION = {u'SPA3102': u'5.1.10'}


class CiscoPlugin(common_globals['BaseCiscoPlugin']):
    IS_PLUGIN = True
    _COMMON_FILENAMES = ['spa3102.cfg']
    
    pg_associator = common_globals['BaseCiscoPgAssociator'](MODEL_VERSION)
