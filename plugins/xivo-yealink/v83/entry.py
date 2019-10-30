# -*- coding: utf-8 -*-

# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
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
    u'T19P_E2': u'53.83.0.35',
    u'T21P_E2': u'52.83.0.35',
    u'T23P': u'44.83.0.35',
    u'T23G': u'44.83.0.35',
    u'T27P': u'45.83.0.35',
    u'T27G': u'69.83.0.35',
    u'T29G': u'46.83.0.35',
    u'T40P': u'54.83.0.35',
    u'T40G': u'76.83.0.35',
    u'T41P': u'36.83.0.35',
    u'T41S': u'66.83.0.35',
    u'T42G': u'29.83.0.35',
    u'T42S': u'66.83.0.35',
    u'T46G': u'28.83.0.35',
    u'T46S': u'66.83.0.35',
    u'T48G': u'35.83.0.35',
    u'T48S': u'66.83.0.35',
    u'T52S': u'70.83.0.35',
    u'T54S': u'70.83.0.35',
    u'T56A': u'58.83.0.5',
    u'T58': u'58.83.0.5',
    u'W60B': u'77.83.0.10',
}

COMMON_FILES = [
    ('y000000000028.cfg', u'T46-28.83.0.35.rom', 'model.tpl'),
    ('y000000000029.cfg', u'T42-29.83.0.35.rom', 'model.tpl'),
    ('y000000000035.cfg', u'T48-35.83.0.35.rom', 'model.tpl'),
    ('y000000000036.cfg', u'T41-36.83.0.35.rom', 'model.tpl'),
    ('y000000000044.cfg', u'T23-44.83.0.35.rom', 'model.tpl'),
    ('y000000000045.cfg', u'T27-45.83.0.35.rom', 'model.tpl'),
    ('y000000000069.cfg', u'T27G-69.83.0.35.rom', 'model.tpl'),
    ('y000000000046.cfg', u'T29-46.83.0.35.rom', 'model.tpl'),
    ('y000000000052.cfg', u'T21P_E2-52.83.0.35.rom', 'model.tpl'),
    ('y000000000053.cfg', u'T19P_E2-53.83.0.35.rom', 'model.tpl'),
    ('y000000000054.cfg', u'T40-54.83.0.35.rom', 'model.tpl'),
    ('y000000000058.cfg', u'T58V(T56A)-58.83.0.5.rom', 'model.tpl'),
    ('y000000000076.cfg', u'T40G-76.83.0.35.rom', 'model.tpl'),
    ('y000000000066.cfg', u'T46S(T48S,T42S,T41S)-66.83.0.35.rom', 'model.tpl'),
    ('y000000000068.cfg', u'T46S(T48S,T42S,T41S)-66.83.0.35.rom', 'model.tpl'),
    ('y000000000070.cfg', u'T54S(T52S)-70.83.0.35.rom', 'model.tpl'),
]
COMMON_FILES_DECT = [
    ('y000000000077.cfg', u'W60B-77.83.0.10.rom', u'W53H-88.83.0.10.rom', u'W56H-61.83.0.10.rom', 'W60P_W53P.tpl'),
]


class YealinkPlugin(common_globals['BaseYealinkPlugin']):
    IS_PLUGIN = True

    pg_associator = common_globals['BaseYealinkPgAssociator'](MODEL_VERSIONS)

    # Yealink plugin specific stuff

    _COMMON_FILES = COMMON_FILES

    def configure_common(self, raw_config):
        super(YealinkPlugin, self).configure_common(raw_config)
        for filename, fw_filename, fw_w53h_handset_filename, fw_w56h_handset_filename, tpl_filename in COMMON_FILES_DECT:
            tpl = self._tpl_helper.get_template('common/%s' % tpl_filename)
            dst = os.path.join(self._tftpboot_dir, filename)
            raw_config[u'XX_fw_filename'] = fw_filename
            raw_config[u'XX_fw_w53h_handset_filename'] = fw_w53h_handset_filename
            raw_config[u'XX_fw_w56h_handset_filename'] = fw_w56h_handset_filename

            self._tpl_helper.dump(tpl, raw_config, dst, self._ENCODING)
