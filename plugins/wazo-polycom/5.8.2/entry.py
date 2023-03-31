# Copyright (C) 2018-2022 Wazo Authors
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
    'VVX101',
    'VVX150',
    'VVX201',
    'VVX250',
    'VVX300',
    'VVX301',
    'VVX310',
    'VVX311',
    'VVX350',
    'VVX400',
    'VVX401',
    'VVX450',
    'VVX410',
    'VVX411',
    'VVX500',
    'VVX501',
    'VVX600',
    'VVX601',
    'VVX1500',
]


class PolycomPlugin(common_globals['BasePolycomPlugin']):
    IS_PLUGIN = True

    pg_associator = common_globals['BasePolycomPgAssociator'](MODELS)
