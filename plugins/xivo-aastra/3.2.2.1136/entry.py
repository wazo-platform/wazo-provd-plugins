# -*- coding: UTF-8 -*-

import logging

common = {}
execfile_('common.py', common)

logger = logging.getLogger('plugin.xivo-aastra')


MODELS = [u'6730i', u'6731i', u'6739i', u'6753i', u'6755i', u'6757i',
          u'9143i', u'9480i']
VERSION = u'3.2.2.1136'


class AastraPlugin(common['BaseAastraPlugin']):
    IS_PLUGIN = True

    pg_associator = common['BaseAastraPgAssociator'](MODELS, VERSION)

    def _add_parking(self, raw_config):
        # hack to set the per line parking config if a park function key is used
        parking = None
        is_parking_set = False
        for funckey_no, funckey_dict in raw_config[u'funckeys'].iteritems():
            if funckey_dict[u'type'] == u'park':
                if is_parking_set:
                    cur_parking = funckey_dict[u'value']
                    if cur_parking != parking:
                        logger.warning('Ignoring park value %s for function key %s: using %s',
                                       cur_parking, funckey_no, parking)
                else:
                    parking = funckey_dict[u'value']
                    is_parking_set = True
                    self._do_add_parking(raw_config, parking)

    def _do_add_parking(self, raw_config, parking):
        raw_config[u'XX_parking'] = u'\n'.join(u'sip line%s park pickup config: %s;%s;asterisk' %
                                               (line_no, parking, parking)
                                               for line_no in raw_config[u'sip_lines'])
