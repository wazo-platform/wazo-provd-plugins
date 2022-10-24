# Copyright 2013-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import os

common_globals = {}
execfile_('common.py', common_globals)

MODEL_VERSIONS = {
    'T19P_E2': '53.81.0.110',
    'T21P_E2': '52.81.0.110',
    'T23P': '44.81.0.110',
    'T23G': '44.81.0.110',
    'T27P': '45.81.0.110',
    'T27G': '69.81.0.110',
    'T29G': '46.81.0.110',
    'T40P': '54.81.0.110',
    'T40G': '76.81.0.110',
    'T41P': '36.81.0.110',
    'T41S': '66.81.0.110',
    'T42G': '29.81.0.110',
    'T42S': '66.81.0.110',
    'T46G': '28.81.0.110',
    'T46S': '66.81.0.110',
    'T48G': '35.81.0.110',
    'T48S': '66.81.0.110',
    'CP860': '37.81.0.10',
    'CP920': '78.81.0.15',
    'W52P': '25.81.0.60',
}

COMMON_FILES = [
    ('y000000000028.cfg', 'T46-28.81.0.110.rom', 'model.tpl'),
    ('y000000000029.cfg', 'T42-29.81.0.110.rom', 'model.tpl'),
    ('y000000000035.cfg', 'T48-35.81.0.110.rom', 'model.tpl'),
    ('y000000000036.cfg', 'T41-36.81.0.110.rom', 'model.tpl'),
    ('y000000000044.cfg', 'T23-44.81.0.110.rom', 'model.tpl'),
    ('y000000000045.cfg', 'T27-45.81.0.110.rom', 'model.tpl'),
    ('y000000000069.cfg', 'T27G-69.81.0.110.rom', 'model.tpl'),
    ('y000000000046.cfg', 'T29-46.81.0.110.rom', 'model.tpl'),
    ('y000000000052.cfg', 'T21P_E2-52.81.0.110.rom', 'model.tpl'),
    ('y000000000053.cfg', 'T19P_E2-53.81.0.110.rom', 'model.tpl'),
    ('y000000000054.cfg', 'T40-54.81.0.110.rom', 'model.tpl'),
    ('y000000000076.cfg', 'T40G-76.81.0.110.rom', 'model.tpl'),
    ('y000000000068.cfg', 'T41S-68.81.0.110.rom', 'model.tpl'),
    ('y000000000067.cfg', 'T42S-67.81.0.110.rom', 'model.tpl'),
    ('y000000000066.cfg', 'T46S-66.81.0.110.rom', 'model.tpl'),
    ('y000000000065.cfg', 'T48S-65.81.0.110.rom', 'model.tpl'),
    ('y000000000037.cfg', 'CP860-37.81.0.10.rom', 'model.tpl'),
    ('y000000000078.cfg', 'CP920-78.81.0.15.rom', 'model.tpl'),
]

COMMON_FILES_DECT = [
    ('y000000000025.cfg', 'Base-W52P-W56P-25.81.0.60.rom', 'W56H-61.81.0.30.rom', 'W52P.tpl'),
]


class YealinkPlugin(common_globals['BaseYealinkPlugin']):
    IS_PLUGIN = True

    pg_associator = common_globals['BaseYealinkPgAssociator'](MODEL_VERSIONS)

    # Yealink plugin specific stuff

    _COMMON_FILES = COMMON_FILES

    def configure_common(self, raw_config):
        super(YealinkPlugin, self).configure_common(raw_config)
        for filename, fw_filename, fw_handset_filename, tpl_filename in COMMON_FILES_DECT:
            tpl = self._tpl_helper.get_template(f'common/{tpl_filename}')
            dst = os.path.join(self._tftpboot_dir, filename)
            raw_config['XX_fw_filename'] = fw_filename
            raw_config['XX_fw_handset_filename'] = fw_handset_filename
            self._tpl_helper.dump(tpl, raw_config, dst, self._ENCODING)
