# Copyright (C) 2013-2022 The Wazo Authors  (see the AUTHORS file)
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

"""Plugin for Avaya 1220IP and 1230IP using the 04.01.13.00 SIP software."""

common_globals = {}
execfile_('common.py', common_globals)


MODELS = ['1220IP', '1230IP']
VERSION = '04.01.13.00'


class AvayaPlugin(common_globals['BaseAvayaPlugin']):
    IS_PLUGIN = True

    pg_associator = common_globals['BaseAvayaPgAssociator'](MODELS, VERSION)
