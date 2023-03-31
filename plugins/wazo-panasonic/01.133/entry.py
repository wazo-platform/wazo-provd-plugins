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

import logging

common = {}
execfile_('common.py', common)

logger = logging.getLogger('plugin.wazo-panasonic')


MODELS = ['KX-UT113', 'KX-UT123', 'KX-UT133', 'KX-UT136']
VERSION = '01.133'


class PanasonicPlugin(common['BasePanasonicPlugin']):
    IS_PLUGIN = True

    _MODELS = MODELS

    pg_associator = common['BasePanasonicPgAssociator'](MODELS, VERSION)
