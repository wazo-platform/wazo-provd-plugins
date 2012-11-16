# -*- coding: UTF-8 -*-

"""Plugin for Cisco SPA8800 in version 6.1.7."""

common_globals = {}
execfile_('common.py', common_globals)


MODEL_VERSION = {u'SPA8800': u'6.1.7'}


class CiscoPlugin(common_globals['BaseCiscoPlugin']):
    IS_PLUGIN = True
    _COMMON_FILENAMES = ['spa8800.cfg']
    
    pg_associator = common_globals['BaseCiscoPgAssociator'](MODEL_VERSION)
