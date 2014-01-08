# -*- coding: utf-8 -*-

# Copyright (C) 2014 Avencall
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

MODEL_VERSION = {
    u'SPA901': u'5.1.5',
    u'SPA921': u'5.1.8',
    u'SPA922': u'6.1.5(a)',
    u'SPA941': u'5.1.8',
    u'SPA942': u'6.1.5(a)',
    u'SPA962': u'6.1.5(a)',
}


class CiscoPlugin(common_globals['BaseCiscoPlugin']):
    IS_PLUGIN = True

    _ENCODING = 'ISO-8859-1'
    _COMMON_FILENAMES = [model.lower().encode('ascii') + '.cfg' for model in
                         MODEL_VERSION]

    pg_associator = common_globals['BaseCiscoPgAssociator'](MODEL_VERSION)
