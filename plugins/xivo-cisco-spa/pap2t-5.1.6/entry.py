# -*- coding: UTF-8 -*-

"""Plugin for Cisco PAP2T in version 5.1.6."""

common_globals = {}
execfile_('common.py', common_globals)


MODEL_VERSION = {u'PAP2T': u'5.1.6'}


class CiscoPlugin(common_globals['BaseCiscoPlugin']):
    IS_PLUGIN = True
    _COMMON_FILENAMES = ['init.cfg']
    
    pg_associator = common_globals['BaseCiscoPgAssociator'](MODEL_VERSION)
