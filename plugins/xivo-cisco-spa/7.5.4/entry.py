# -*- coding: UTF-8 -*-

common_globals = {}
execfile_('common.py', common_globals)

PSN = [u'301', u'303', u'501G', u'502G', u'504G', u'508G', u'509G', u'525G', u'525G2']
MODELS = [u'SPA' + psn for psn in PSN]
MODEL_VERSION = dict((model, u'7.5.4') for model in MODELS)


class CiscoPlugin(common_globals['BaseCiscoPlugin']):
    IS_PLUGIN = True
    # similar to spa508G.cfg (G is uppercase)
    _COMMON_FILENAMES = ['spa' + psn.encode('ascii') + '.cfg' for psn in PSN]

    pg_associator = common_globals['BaseCiscoPgAssociator'](MODEL_VERSION)
