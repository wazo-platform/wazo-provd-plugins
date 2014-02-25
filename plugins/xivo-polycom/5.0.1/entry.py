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

MODELS = [
    u'VVX300',
    u'VVX310',
    u'VVX400',
    u'VVX410',
    u'VVX500',
    u'VVX600',
    u'VVX1500',
]
VERSION = u'5.0.1.7310'


class PolycomPlugin(common_globals['BasePolycomPlugin']):
    IS_PLUGIN = True

    pg_associator = common_globals['BasePolycomPgAssociator'](MODELS, VERSION)
