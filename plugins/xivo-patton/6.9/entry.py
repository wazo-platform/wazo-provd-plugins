# -*- coding: utf-8 -*-

# Copyright (C) 2016 Avencall
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
    u'SN4112',
    u'SN4114',
    u'SN4116',
    u'SN4118',
    u'SN4316',
    u'SN4324',
    u'SN4332',
]
VERSION = u'6.9'


class PattonPlugin(common['BasePattonPlugin']):
    IS_PLUGIN = True

    pg_associator = common['BasePattonPgAssociator'](MODELS, VERSION)
