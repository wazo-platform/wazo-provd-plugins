# -*- coding: UTF-8 -*-

"""Plugin for legacy Cisco SPA phones. This include every Linksys branded
phones.

The following Cisco phones are supported:
- SPA901
- SPA921
- SPA922
- SPA941
- SPA942
- SPA962

The following Cisco expansion module are supported:
- SPA932

"""

common_globals = {}
execfile_('common.py', common_globals)


MODEL_VERSION = {u'SPA901': u'5.1.5',
                 u'SPA921': u'5.1.8',
                 u'SPA922': u'6.1.5(a)',
                 u'SPA941': u'5.1.8',
                 u'SPA942': u'6.1.5(a)',
                 u'SPA962': u'6.1.5(a)'}


class CiscoPlugin(common_globals['BaseCiscoPlugin']):
    IS_PLUGIN = True

    _ENCODING = 'ISO-8859-1'
    _COMMON_FILENAMES = [model.lower().encode('ascii') + '.cfg' for model in
                         MODEL_VERSION]

    pg_associator = common_globals['BaseCiscoPgAssociator'](MODEL_VERSION)
