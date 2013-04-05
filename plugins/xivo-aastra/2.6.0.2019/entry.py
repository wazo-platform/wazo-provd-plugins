# -*- coding: UTF-8 -*-

common = {}
execfile_('common.py', common)


MODELS = [u'6730i', u'6731i', u'6751i', u'6753i', u'6755i', u'6757i',
          u'9143i', u'9480i']
MODEL_VERSIONS = dict((model, u'2.6.0.2019') for model in MODELS)


class AastraPlugin(common['BaseAastraPlugin']):
    IS_PLUGIN = True

    pg_associator = common['BaseAastraPgAssociator'](MODEL_VERSIONS)
