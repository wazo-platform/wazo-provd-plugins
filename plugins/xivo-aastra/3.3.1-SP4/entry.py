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

import logging

common = {}
execfile_('common.py', common)

logger = logging.getLogger('plugin.xivo-aastra')


MODEL_VERSIONS = {
    u'6730i': u'3.3.1.4322',
    u'6731i': u'3.3.1.4322',
    u'6735i': u'3.3.1.8154',
    u'6737i': u'3.3.1.8154',
    u'6739i': u'3.3.1.4322',
    u'6753i': u'3.3.1.4322',
    u'6755i': u'3.3.1.4322',
    u'6757i': u'3.3.1.4322',
    u'9143i': u'3.3.1.4295',
    u'9480i': u'3.3.1.4295',
}


class AastraPlugin(common['BaseAastraPlugin']):
    IS_PLUGIN = True
    _LANGUAGE_PATH = 'i18n/'

    pg_associator = common['BaseAastraPgAssociator'](MODEL_VERSIONS)
