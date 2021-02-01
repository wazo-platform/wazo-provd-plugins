# -*- coding: utf-8 -*-

# Copyright 2013-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import os

common_globals = {}
execfile_('common.py', common_globals)

MODEL_VERSIONS = {
    u'CP960': u'73.83.0.30',
    u'T29G': u'46.83.0.120',
    u'T41P': u'36.83.0.35',
    u'T42G': u'29.83.0.120',
    u'T46G': u'28.83.0.120',
    u'T48G': u'35.83.0.120',
    u'T56A': u'58.83.0.15',
    u'T58': u'58.83.0.15',
    u'W60B': u'77.83.0.85',
    u'W80B': u'103.83.0.80',
    u'W80DM': u'103.83.0.80',
}

COMMON_FILES = [
    ('y000000000028.cfg', u'T46-28.83.0.120.rom', 'model.tpl'),
    ('y000000000029.cfg', u'T42-29.83.0.120.rom', 'model.tpl'),
    ('y000000000035.cfg', u'T48-35.83.0.120.rom', 'model.tpl'),
    ('y000000000036.cfg', u'T41-36.83.0.120.rom', 'model.tpl'),
    ('y000000000046.cfg', u'T29-46.83.0.120.rom', 'model.tpl'),
    ('y000000000058.cfg', u'T58V(T56A)-58.83.0.15.rom', 'model.tpl'),
    ('y000000000073.cfg', u'CP960-73.83.0.30.rom', 'model.tpl'),
]

HANDSETS_FW = {
    'w53h': u'W53H-88.83.0.90.rom',
    'w56h': u'W56H-61.83.0.90.rom',
    'w59r': u'W59R-115.83.0.10.rom',
    'cp930w': u'CP930W-87.83.0.60.rom',
}

COMMON_FILES_DECT = [
    {
        'filename': u'y000000000077.cfg',
        'fw_filename': u'W60B-77.83.0.85.rom',
        'handsets_fw': HANDSETS_FW,
        'tpl_filename': u'dect_model.tpl',
    },
    {
        'filename': u'y000000000103.cfg',
        'fw_filename': u'$PN-103.83.0.80.rom',  # $PN = Product Name, i.e W80B/W80DM
        'handsets_fw': HANDSETS_FW,
        'tpl_filename': u'dect_model.tpl',
    }
]


class YealinkPlugin(common_globals['BaseYealinkPlugin']):
    IS_PLUGIN = True

    pg_associator = common_globals['BaseYealinkPgAssociator'](MODEL_VERSIONS)

    # Yealink plugin specific stuff

    _COMMON_FILES = COMMON_FILES

    def configure_common(self, raw_config):
        super(YealinkPlugin, self).configure_common(raw_config)
        for dect_info in COMMON_FILES_DECT:
            tpl = self._tpl_helper.get_template('common/%s' % dect_info[u'tpl_filename'])
            dst = os.path.join(self._tftpboot_dir, dect_info[u'filename'])
            raw_config[u'XX_handsets_fw'] = dect_info[u'handsets_fw']
            raw_config[u'XX_fw_filename'] = dect_info[u'fw_filename']

            self._tpl_helper.dump(tpl, raw_config, dst, self._ENCODING)
