# -*- coding: utf-8 -*-

# Copyright 2013-2020 The Wazo Authors  (see the AUTHORS file)
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

common = {}
execfile_('common.py', common)

MODELS = [
    u'7906G',
    u'7911G',
    u'7931G',
    u'7941G',
    u'7942G',
    u'7945G',
    u'7961G',
    u'7962G',
    u'7965G',
    u'7970G',
    u'7971G',
]


class CiscoSccpPlugin(common['BaseCiscoSccpPlugin']):
    IS_PLUGIN = True

    pg_associator = common['BaseCiscoPgAssociator'](MODELS)
