# -*- coding: UTF-8 -*-

common = {}
execfile_('common.py', common)


VERSION = u'1.1.0.0.48178'


class DigiumPlugin(common['BaseDigiumPlugin']):
    IS_PLUGIN = True

    pg_associator = common['DigiumPgAssociator'](VERSION)

