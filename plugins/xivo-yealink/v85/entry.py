# -*- coding: utf-8 -*-

# Copyright 2013-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import os

common_globals = {}
execfile_('common.py', common_globals)

MODEL_VERSIONS = {
    u'T30': u'124.85.0.15',
    u'T30P': u'124.85.0.15',
    u'T31': u'124.85.0.15',
    u'T31P': u'124.85.0.15',
    u'T31G': u'124.85.0.15',
    u'T33P': u'124.85.0.15',
    u'T33G': u'124.85.0.15',
    u'W90DM': u'130.85.0.15',
    u'W90B': u'130.85.0.15',
}

COMMON_FILES = [
    ('y0000000000123.cfg', u'T31(T30,T30P,T31G,T31P,T33P,T33G)-124.85.0.15.rom', 'model.tpl'),
    ('y0000000000124.cfg', u'T31(T30,T30P,T31G,T31P,T33P,T33G)-124.85.0.15.rom', 'model.tpl'),
    ('y0000000000127.cfg', u'T31(T30,T30P,T31G,T31P,T33P,T33G)-124.85.0.15.rom', 'model.tpl'),
]

COMMON_FILES_DECT = [
    {
        'filename': u'y000000000130.cfg',
        'fw_filename': u'$PN-130.85.0.15.rom',  # $PN = Product Name, i.e W90B/W90DM
        'handsets_fw': {
            'w53h': u'W53H-88.85.0.20.rom',
            'w56h': u'W56H-61.85.0.20.rom',
            'w59r': u'W59R-115.85.0.20.rom',
            'cp930w': u'CP930W-87.85.0.20.rom',
        },
        'tpl_filename': u'dect_model.tpl',
    },
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
