# -*- coding: UTF-8 -*-

common_globals = {}
execfile_('common.py', common_globals)


MODELS = [u'300', u'320', u'360', u'370', u'710', u'720', u'760', u'820', u'821', u'870', u'MP', u'PA1']
VERSION = u'8.7.3.15'


class SnomPlugin(common_globals['BaseSnomPlugin']):
    IS_PLUGIN = True

    _MODELS = MODELS

    pg_associator = common_globals['BaseSnomPgAssociator'](MODELS, VERSION)
