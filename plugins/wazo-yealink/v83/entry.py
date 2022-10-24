# Copyright 2013-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import os

common_globals = {}
execfile_('common.py', common_globals)

# commented values are repeated values that are then overriden
MODEL_VERSIONS = {
    'T19P_E2': '53.83.0.35',
    'T21P_E2': '52.83.0.35',
    'T23P': '44.83.0.35',
    'T23G': '44.83.0.35',
    'T27P': '45.83.0.35',
    'T27G': '69.83.0.35',
    'T40P': '54.83.0.35',
    'T40G': '76.83.0.35',
    'CP960': '73.83.0.30',
    'T29G': '46.83.0.120',
    'T41P': '36.83.0.35',
    'T41S': '66.83.0.35',
    'T42S': '66.83.0.35',
    'T46S': '66.83.0.35',
    'T48S': '66.83.0.35',
    'T52S': '70.83.0.35',
    'T54S': '70.83.0.35',
    'T42G': '29.83.0.120',
    'T46G': '28.83.0.120',
    'T48G': '35.83.0.120',
    'T56A': '58.83.0.15',
    'T58': '58.83.0.15',
    'W60B': '77.83.0.85',
    'W80B': '103.83.0.122',
    'W80DM': '103.83.0.122',
}

COMMON_FILES = [
    ('y000000000044.cfg', 'T23-44.83.0.35.rom', 'model.tpl'),
    ('y000000000045.cfg', 'T27-45.83.0.35.rom', 'model.tpl'),
    ('y000000000069.cfg', 'T27G-69.83.0.35.rom', 'model.tpl'),
    ('y000000000052.cfg', 'T21P_E2-52.83.0.35.rom', 'model.tpl'),
    ('y000000000053.cfg', 'T19P_E2-53.83.0.35.rom', 'model.tpl'),
    ('y000000000054.cfg', 'T40-54.83.0.35.rom', 'model.tpl'),
    ('y000000000076.cfg', 'T40G-76.83.0.35.rom', 'model.tpl'),
    ('y000000000066.cfg', 'T46S(T48S,T42S,T41S)-66.83.0.35.rom', 'model.tpl'),
    ('y000000000068.cfg', 'T46S(T48S,T42S,T41S)-66.83.0.35.rom', 'model.tpl'),
    ('y000000000070.cfg', 'T54S(T52S)-70.83.0.35.rom', 'model.tpl'),
    ('y000000000028.cfg', 'T46-28.83.0.120.rom', 'model.tpl'),
    ('y000000000029.cfg', 'T42-29.83.0.120.rom', 'model.tpl'),
    ('y000000000035.cfg', 'T48-35.83.0.120.rom', 'model.tpl'),
    ('y000000000036.cfg', 'T41-36.83.0.120.rom', 'model.tpl'),
    ('y000000000046.cfg', 'T29-46.83.0.120.rom', 'model.tpl'),
    ('y000000000058.cfg', 'T58V(T56A)-58.83.0.15.rom', 'model.tpl'),
    ('y000000000073.cfg', 'CP960-73.83.0.30.rom', 'model.tpl'),
]

HANDSETS_FW = {
    'w53h': 'W53H-88.83.0.90.rom',
    'w56h': 'W56H-61.83.0.90.rom',
    'w59r': 'W59R-115.83.0.10.rom',
    'cp930w': 'CP930W-87.83.0.60.rom',
}

COMMON_FILES_DECT = [
    {
        'filename': 'y000000000077.cfg',
        'fw_filename': 'W60B-77.83.0.85.rom',
        'handsets_fw': HANDSETS_FW,
        'tpl_filename': 'dect_model.tpl',
    },
    {
        'filename': 'y000000000103.cfg',
        'fw_filename': '$PN-103.83.0.122.rom',  # $PN = Product Name, i.e W80B
        'handsets_fw': HANDSETS_FW,
        'tpl_filename': 'dect_model.tpl',
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
            tpl = self._tpl_helper.get_template(f'common/{dect_info["tpl_filename"]}')
            dst = os.path.join(self._tftpboot_dir, dect_info['filename'])
            raw_config['XX_handsets_fw'] = dect_info['handsets_fw']
            raw_config['XX_fw_filename'] = dect_info['fw_filename']

            self._tpl_helper.dump(tpl, raw_config, dst, self._ENCODING)
