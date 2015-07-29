# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import logging
import os

common_globals = {}
execfile_('common.py', common_globals)

logger = logging.getLogger('plugin.xivo-yealink')

MODEL_VERSIONS = {
    u'T19P_E2': u'53.80.0.60',
    u'T21P_E2': u'52.80.0.60',
    u'T41P': u'36.80.0.60',
    u'T42G': u'29.80.0.60',
    u'T46G': u'28.80.0.60',
    u'T48G': u'35.80.0.60',
}
MODEL_SIP_ACCOUNTS = {
    u'T19P_E2': 1,
    u'T21P_E2': 2,
    u'T41P': 6,
    u'T42G': 12,
    u'T46G': 16,
    u'T48G': 16,
}
COMMON_FILES = [
    ('y000000000028.cfg', u'28.80.0.60.rom', 'model.tpl'),
    ('y000000000029.cfg', u'29.80.0.60.rom', 'model.tpl'),
    ('y000000000035.cfg', u'35.80.0.60.rom', 'model.tpl'),
    ('y000000000036.cfg', u'36.80.0.60.rom', 'model.tpl'),
    ('y000000000052.cfg', u'52.80.0.60.rom', 'model.tpl'),
    ('y000000000053.cfg', u'53.80.0.60.rom', 'model.tpl'),
]


class YealinkPlugin(common_globals['BaseYealinkPlugin']):
    IS_PLUGIN = True

    pg_associator = common_globals['BaseYealinkPgAssociator'](MODEL_VERSIONS)

    # Yealink plugin specific stuff

    _COMMON_FILES = COMMON_FILES

    def _add_fkeys(self, raw_config, device):
        lines = []
        funckeys = raw_config[u'funckeys']
        exten_pickup_call = raw_config.get('exten_pickup_call')
        model = device.get(u'model')
        prefixes = _FunckeyPrefixIterator(model)
        for funckey_no, prefix in enumerate(prefixes, start=1):
            funckey = funckeys.get(unicode(funckey_no))
            self._format_funckey(lines, funckey_no, model, prefix, funckey, exten_pickup_call)
            lines.append(u'')

        raw_config[u'XX_fkeys'] = u'\n'.join(lines)

    def _format_funckey(self, lines, funckey_no, model, prefix, funckey, exten_pickup_call):
        if funckey is None:
            if funckey_no == 1 and model == u'T46G':
                self._format_funckey_line(lines, prefix)
            else:
                self._format_funckey_null(lines, prefix)
            return

        funckey_type = funckey[u'type']
        if funckey_type == u'speeddial':
            self._format_funckey_speeddial(lines, prefix, funckey)
        elif funckey_type == u'blf':
            self._format_funckey_blf(lines, prefix, funckey, exten_pickup_call)
        elif funckey_type == u'park':
            self._format_funckey_park(lines, prefix, funckey)
        else:
            logger.info('Unsupported funckey type: %s', funckey_type)

    def _format_funckey_null(self, lines, prefix):
        lines.append(u'%s.type = %%NULL%%' % prefix)
        lines.append(u'%s.line = %%NULL%%' % prefix)
        lines.append(u'%s.value = %%NULL%%' % prefix)
        lines.append(u'%s.label = %%NULL%%' % prefix)

    def _format_funckey_speeddial(self, lines, prefix, funckey):
        lines.append(u'%s.type = 13' % prefix)
        lines.append(u'%s.line = %s' % (prefix, funckey.get(u'line', 1)))
        lines.append(u'%s.value = %s' % (prefix, funckey[u'value']))
        lines.append(u'%s.label = %s' % (prefix, funckey.get(u'label', u'')))

    def _format_funckey_park(self, lines, prefix, funckey):
        lines.append(u'%s.type = 10' % prefix)
        lines.append(u'%s.line = %s' % (prefix, funckey.get(u'line', 1)))
        lines.append(u'%s.value = %s' % (prefix, funckey[u'value']))
        lines.append(u'%s.label = %s' % (prefix, funckey.get(u'label', u'')))

    def _format_funckey_blf(self, lines, prefix, funckey, exten_pickup_call):
        lines.append(u'%s.type = 16' % prefix)
        lines.append(u'%s.line = %s' % (prefix, funckey.get(u'line', 1)))
        lines.append(u'%s.value = %s' % (prefix, funckey[u'value']))
        lines.append(u'%s.label = %s' % (prefix, funckey.get(u'label', u'')))
        if exten_pickup_call:
            lines.append(u'%s.pickup_value = %s' % (prefix, exten_pickup_call))

    def _format_funckey_line(self, lines, prefix):
        lines.append(u'%s.type = 15' % prefix)
        lines.append(u'%s.line = 1' % prefix)
        lines.append(u'%s.value = %%NULL%%' % prefix)
        lines.append(u'%s.label = %%NULL%%' % prefix)

    def _get_sip_accounts(self, model):
        return MODEL_SIP_ACCOUNTS.get(model)


class _FunckeyPrefixIterator(object):

    _NB_LINEKEY = {
        u'T19P_E2': 0,
        u'T21P_E2': 2,
        u'T41P': 15,
        u'T42G': 15,
        u'T46G': 27,
        u'T48G': 27,
    }
    _NB_MEMORYKEY = {
        u'T19P_E2': 0,
        u'T21P_E2': 0,
        u'T41P': 0,
        u'T42G': 0,
        u'T46G': 0,
        u'T48G': 0,
    }
    _NB_EXPMODKEY = 40

    def __init__(self, model):
        self._nb_linekey = self._nb_linekey_by_model(model)
        self._nb_memorykey = self._nb_memorykey_by_model(model)
        self._nb_expmod = self._nb_expmod_by_model(model)

    def _nb_linekey_by_model(self, model):
        if model is None:
            logger.info('No model information; no linekey will be configured')
            return 0
        nb_linekey = self._NB_LINEKEY.get(model)
        if nb_linekey is None:
            logger.info('Unknown model %s; no linekey will be configured', model)
            return 0
        return nb_linekey

    def _nb_memorykey_by_model(self, model):
        if model is None:
            logger.info('No model information; no memorykey will be configured')
            return 0
        nb_memorykey = self._NB_MEMORYKEY.get(model)
        if nb_memorykey is None:
            logger.info('Unknown model %s; no memorykey will be configured', model)
            return 0
        return nb_memorykey

    def _nb_expmod_by_model(self, model):
        if model in (u'T46G', u'T48G'):
            return 6
        else:
            return 0

    def __iter__(self):
        for linekey_no in xrange(1, self._nb_linekey + 1):
            yield u'linekey.%s' % linekey_no
        for memorykey_no in xrange(1, self._nb_memorykey + 1):
            yield u'memorykey.%s' % memorykey_no
        for expmod_no in xrange(1, self._nb_expmod + 1):
            for expmodkey_no in xrange(1, self._NB_EXPMODKEY + 1):
                yield u'expansion_module.%s.key.%s' % (expmod_no, expmodkey_no)
