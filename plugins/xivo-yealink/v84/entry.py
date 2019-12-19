# -*- coding: utf-8 -*-

# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import os

common_globals = {}
execfile_('common.py', common_globals)

MODEL_VERSIONS = {
    u'CP920': u'78.84.0.15',
    u'T19P_E2': u'53.84.0.15',
    u'T21P_E2': u'52.84.0.15',
    u'T23P': u'44.84.0.15',
    u'T23G': u'44.84.0.15',
    u'T27G': u'69.84.0.15',
    u'T40P': u'54.84.0.15',
    u'T40G': u'76.84.0.15',
    u'T41S': u'66.84.0.15',
    u'T42S': u'66.84.0.15',
    u'T46S': u'66.84.0.15',
    u'T48S': u'66.84.0.15',
    u'T52S': u'70.84.0.15',
    u'T53': u'95.84.0.30',
    u'T53W': u'95.84.0.30',
    u'T54S': u'70.84.0.15',
    u'T54W': u'96.84.0.30',
    u'T57W': u'97.84.0.85',
    u'W52P': u'25.81.0.30',
    u'W60B': u'77.83.0.10',
    u'W80B': u'103.83.0.50',

}

COMMON_FILES = [
    ('y000000000044.cfg', u'T23-44.84.0.15.rom', 'model.tpl'),
    ('y000000000069.cfg', u'T27G-69.84.0.15.rom', 'model.tpl'),
    ('y000000000052.cfg', u'T21P_E2-52.84.0.15.rom', 'model.tpl'),
    ('y000000000053.cfg', u'T19P_E2-53.84.0.15.rom', 'model.tpl'),
    ('y000000000054.cfg', u'T40-54.84.0.15.rom', 'model.tpl'),
    ('y000000000076.cfg', u'T40G-76.84.0.15.rom', 'model.tpl'),
    ('y000000000065.cfg', u'T46S(T48S,T42S,T41S)-66.84.0.15.rom', 'model.tpl'),
    ('y000000000066.cfg', u'T46S(T48S,T42S,T41S)-66.84.0.15.rom', 'model.tpl'),
    ('y000000000067.cfg', u'T46S(T48S,T42S,T41S)-66.84.0.15.rom', 'model.tpl'),
    ('y000000000068.cfg', u'T46S(T48S,T42S,T41S)-66.84.0.15.rom', 'model.tpl'),
    ('y000000000095.cfg', u'T53W(T53)-95.84.0.30.rom', 'model.tpl'),
    ('y000000000070.cfg', u'T54S(T52S)-70.84.0.15.rom', 'model.tpl'),
    ('y000000000078.cfg', u'CP920-78.84.0.15.rom', 'model.tpl'),
]


COMMON_FILES_DECT = [
    ('y000000000025.cfg', u'Base-W52P-W56P-25.81.0.30.rom', u'W52H-26.81.0.50.rom', u'', u'W56H-61.83.0.10.rom', u'', u'', 'W52H_W56H-W52P.tpl'),
    ('y000000000077.cfg', u'W60B-77.83.0.10.rom', u'W52H-26.81.0.50.rom', u'W53H-88.83.0.10.rom', u'W56H-61.83.0.10.rom', u'', u'', 'W52H_W53H_W56H-W60B.tpl'),
    ('y000000000103.cfg', u'W80B-103.83.0.50.rom', u'', u'', u'', u'W53H-88.83.0.80.rom', u'W56H-61.83.0.80.rom', 'W53H_W56H-W80B.tpl'),
    ('y000000000096.cfg', u'T54W-96.84.0.30.rom', u'W52H-26.81.0.50.rom', u'W53H-88.83.0.10.rom', u'W56H-61.83.0.10.rom', u'', u'', 'W52H_W53H_W56H-T54W.tpl'),
    ('y000000000097.cfg', u'T57W-97.84.0.85.rom', u'W52H-26.81.0.50.rom', u'W53H-88.83.0.10.rom', u'W56H-61.83.0.10.rom', u'', u'', 'W52H_W53H_W56H-T57W.tpl'),
]

class YealinkPlugin(common_globals['BaseYealinkPlugin']):
    IS_PLUGIN = True

    pg_associator = common_globals['BaseYealinkPgAssociator'](MODEL_VERSIONS)

    # Yealink plugin specific stuff

    _COMMON_FILES = COMMON_FILES

    def configure_common(self, raw_config):
        super(YealinkPlugin, self).configure_common(raw_config)
        for filename, fw_filename, fw_w52h_handset_filename, fw_w53h_handset_filename, fw_w56h_handset_filename, fw_w53h_w80b_handset_filename, fw_w56h_w80b_handset_filename, tpl_filename in COMMON_FILES_DECT:
            tpl = self._tpl_helper.get_template('common/%s' % tpl_filename)
            dst = os.path.join(self._tftpboot_dir, filename)
            raw_config[u'XX_fw_filename'] = fw_filename
            raw_config[u'XX_fw_w52h_handset_filename'] = fw_w52h_handset_filename
            raw_config[u'XX_fw_w53h_handset_filename'] = fw_w53h_handset_filename
            raw_config[u'XX_fw_w56h_handset_filename'] = fw_w56h_handset_filename
            raw_config[u'XX_fw_w53h_w80b_handset_filename'] = fw_w53h_w80b_handset_filename
            raw_config[u'XX_fw_w56h_w80b_handset_filename'] = fw_w56h_w80b_handset_filename
            
            self._tpl_helper.dump(tpl, raw_config, dst, self._ENCODING)
