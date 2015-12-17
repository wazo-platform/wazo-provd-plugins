# -*- coding: utf-8 -*-

# Copyright (C) 2014-2015 Avencall
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

MODELS = [
    u'710',
    u'715',
    u'720',
    u'725',
    u'760',
    u'D765',
    u'821',
]
VERSION = u'8.7.5.35'


class SnomPlugin(common_globals['BaseSnomPlugin']):
    IS_PLUGIN = True

    _MODELS = MODELS

    pg_associator = common_globals['BaseSnomPgAssociator'](MODELS, VERSION)
