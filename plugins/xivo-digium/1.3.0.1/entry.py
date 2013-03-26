# -*- coding: UTF-8 -*-

common = {}
execfile_('common.py', common)


VERSION = u'1.3.0.1.53901'


class DigiumPlugin(common['BaseDigiumPlugin']):
    IS_PLUGIN = True

    pg_associator = common['DigiumPgAssociator'](VERSION)

