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

import os

common_globals = {}
execfile_('common.py', common_globals)

MODEL_VERSIONS = {
    u'T20P': u'9.73.0.50',
    u'T22P': u'7.73.0.50',
    u'T26P': u'6.73.0.50',
    u'T28P': u'2.73.0.50',
    u'W52P': u'25.73.0.40',
}
COMMON_FILES = [
    ('y000000000000.cfg', u'2.73.0.50.rom', 'model-M7+M1.tpl'),
    ('y000000000004.cfg', u'6.73.0.50.rom', 'model-M7+M1.tpl'),
    ('y000000000005.cfg', u'7.73.0.50.rom', 'model-M7+M1.tpl'),
    ('y000000000007.cfg', u'9.73.0.50.rom', 'model-M7+M1.tpl'),
]
COMMON_FILES_DECT = [
    ('y000000000025.cfg', u'25.73.0.40.rom', u'26.73.0.11.rom', 'W52P.tpl'),
]


class YealinkPlugin(common_globals['BaseYealinkPlugin']):
    IS_PLUGIN = True

    pg_associator = common_globals['BaseYealinkPgAssociator'](MODEL_VERSIONS)

    # Yealink plugin specific stuff

    _COMMON_FILES = COMMON_FILES

    def configure_common(self, raw_config):
        super(YealinkPlugin, self).configure_common(raw_config)
        for filename, fw_filename, fw_handset_filename, tpl_filename in COMMON_FILES_DECT:
            tpl = self._tpl_helper.get_template('common/%s' % tpl_filename)
            dst = os.path.join(self._tftpboot_dir, filename)
            raw_config[u'XX_fw_filename'] = fw_filename
            raw_config[u'XX_fw_handset_filename'] = fw_handset_filename
            self._tpl_helper.dump(tpl, raw_config, dst, self._ENCODING)
