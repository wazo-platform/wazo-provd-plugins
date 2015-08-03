# -*- coding: utf-8 -*-

# Copyright (C) 2013-2015 Avencall
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

MODEL_VERSIONS = {
    u'T32G': u'32.70.1.33',
    u'T38G': u'38.70.1.33',
    u'VP530P': u'23.70.0.40',
}
COMMON_FILES = [
    ('y000000000023.cfg', u'23.70.0.40-Yealink.rom', 'model-M7+M1.tpl'),
    ('y000000000032.cfg', u'32.70.1.33.rom', 'model-M7+M2.tpl'),
    ('y000000000038.cfg', u'38.70.1.33.rom', 'model-M7+M2.tpl'),
]


class YealinkPlugin(common_globals['BaseYealinkPlugin']):
    IS_PLUGIN = True

    pg_associator = common_globals['BaseYealinkPgAssociator'](MODEL_VERSIONS)

    # Yealink plugin specific stuff

    _COMMON_FILES = COMMON_FILES
