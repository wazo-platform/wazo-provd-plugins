# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
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

common_globals = {}
execfile_('common.py', common_globals)


MODEL_VERSIONS = {u'T41P': u'29.71.0.155', u'T42G': u'36.71.0.155', u'T46G': u'28.71.0.155'}
COMMON_FILES = [('y000000000028.cfg', u'28.71.0.155.rom', 'model.tpl'),
                ('y000000000029.cfg', u'29.71.0.155.rom', 'model.tpl'),
                ('y000000000036.cfg', u'29.71.0.155.rom', 'model.tpl'),
               ]


class YealinkPlugin(common_globals['BaseYealinkPlugin']):
    IS_PLUGIN = True

    pg_associator = common_globals['BaseYealinkPgAssociator'](MODEL_VERSIONS)

    # Yealink plugin specific stuff

    _COMMON_FILES = COMMON_FILES

    def _format_funckey_speeddial(self, funckey_no, funckey_dict):
        lines = []
        lines.append(u'linekey.%s.line = %s' % (funckey_no, funckey_dict.get(u'line', 1)))
        lines.append(u'linekey.%s.value = %s' % (funckey_no, funckey_dict[u'value']))
        lines.append(u'linekey.%s.type = 13' % funckey_no)
        lines.append(u'linekey.%s.label = %s' % (funckey_no, funckey_dict.get(u'label', u'')))
        return lines

    def _format_funckey_blf(self, funckey_no, funckey_dict, exten_pickup_call=None):
        # Be warned that blf works only for DSS keys.
        lines = []
        lines.append(u'linekey.%s.line = %s' % (funckey_no, funckey_dict.get(u'line', 1) - 1))
        value = funckey_dict[u'value']
        lines.append(u'linekey.%s.value = %s' % (funckey_no, value))
        lines.append(u'linekey.%s.label = %s' % (funckey_no, funckey_dict.get(u'label', u'')))
        if exten_pickup_call:
            lines.append(u'linekey.%s.extension = %s' % (funckey_no, exten_pickup_call))
        lines.append(u'linekey.%s.type = 16' % funckey_no)
        return lines

