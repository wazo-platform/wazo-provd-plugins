# -*- coding: utf-8 -*-

# Copyright 2013-2018 The Wazo Authors  (see the AUTHORS file)
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
    u'C58',
    u'C62',
]
COMMON_FILES = [
    ('f0C00580000.cfg', u'C58_V2_3_431_247T20140605184312.z', 'model.tpl'),
    ('f0C00620000.cfg', u'2012070649327421.z', 'model.tpl'),
]


class FanvilPlugin(common['BaseFanvilPlugin']):
    IS_PLUGIN = True

    _COMMON_FILES = COMMON_FILES

    pg_associator = common['BaseFanvilPgAssociator'](MODELS)
