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

import os

common_globals = {}
execfile_('common.py', common_globals)

MODEL_VERSIONS = {
    u'T19P_E2': u'53.81.0.110',
    u'T21P_E2': u'52.81.0.110',
    u'T23P': u'44.81.0.110',
    u'T23G': u'44.81.0.110',
    u'T27P': u'45.81.0.110',
    u'T27G': u'69.81.0.110',
    u'T29G': u'46.81.0.110',
    u'T40P': u'54.81.0.110',
    u'T40G': u'76.81.0.110',
    u'T41P': u'36.81.0.110',
    u'T41S': u'66.81.0.110',
    u'T42G': u'29.81.0.110',
    u'T42S': u'66.81.0.110',
    u'T46G': u'28.81.0.110',
    u'T46S': u'66.81.0.110',
    u'T48G': u'35.81.0.110',
    u'T48S': u'66.81.0.110',
    u'CP860': u'37.81.0.10',
    u'CP920': u'78.81.0.15',
    u'W52P': u'25.81.0.10',
}

COMMON_FILES = [
    ('y000000000028.cfg', u'T46-28.81.0.110.rom', 'model.tpl'),
    ('y000000000029.cfg', u'T42-29.81.0.110.rom', 'model.tpl'),
    ('y000000000035.cfg', u'T48-35.81.0.110.rom', 'model.tpl'),
    ('y000000000036.cfg', u'T41-36.81.0.110.rom', 'model.tpl'),
    ('y000000000044.cfg', u'T23-44.81.0.110.rom', 'model.tpl'),
    ('y000000000045.cfg', u'T27-45.81.0.110.rom', 'model.tpl'),
    ('y000000000069.cfg', u'T27G-69.81.0.110.rom', 'model.tpl'),
    ('y000000000046.cfg', u'T29-46.81.0.110.rom', 'model.tpl'),
    ('y000000000052.cfg', u'T21P_E2-52.81.0.110.rom', 'model.tpl'),
    ('y000000000053.cfg', u'T19P_E2-53.81.0.110.rom', 'model.tpl'),
    ('y000000000054.cfg', u'T40-54.81.0.110.rom', 'model.tpl'),
    ('y000000000076.cfg', u'T40G-76.81.0.110.rom', 'model.tpl'),
    ('y000000000068.cfg', u'T41S-68.81.0.110.rom', 'model.tpl'),
    ('y000000000067.cfg', u'T42S-67.81.0.110.rom', 'model.tpl'),
    ('y000000000066.cfg', u'T46S-66.81.0.110.rom', 'model.tpl'),
    ('y000000000065.cfg', u'T48S-65.81.0.110.rom', 'model.tpl'),
    ('y000000000037.cfg', u'CP860-37.81.0.10.rom', 'model.tpl'),
    ('y000000000078.cfg', u'CP920-78.81.0.15.rom', 'model.tpl'),
]

COMMON_FILES_DECT = [
    ('y000000000025.cfg', u'Base-W52P-W56P-25.81.0.10.rom', u'W56H-61.81.0.30.rom', 'W52P.tpl'),
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

