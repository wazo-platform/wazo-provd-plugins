# -*- coding: UTF-8 -*-

"""Plugin for Cisco SPA8000 in version 6.1.3."""

common_globals = {}
execfile_('common.py', common_globals)


MODEL_VERSION = {u'SPA8000': u'6.1.3'}


class CiscoPlugin(common_globals['BaseCiscoPlugin']):
    IS_PLUGIN = True
    _COMMON_FILENAMES = ['spa8000.cfg']
    
    pg_associator = common_globals['BaseCiscoPgAssociator'](MODEL_VERSION)
