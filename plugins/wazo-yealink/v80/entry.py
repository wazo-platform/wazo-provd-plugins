# Copyright 2013-2023 The Wazo Authors  (see the AUTHORS file)
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
    'T19P_E2': '53.80.0.95',
    'T21P_E2': '52.80.0.95',
    'T23P': '44.80.0.95',
    'T23G': '44.80.0.95',
    'T27P': '45.80.0.95',
    'T29G': '46.80.0.95',
    'T40P': '54.80.0.95',
    'T41P': '36.80.0.95',
    'T42G': '29.80.0.95',
    'T46G': '28.80.0.95',
    'T48G': '35.80.0.95',
    'T49G': '51.80.0.100',
    'CP860': '37.80.0.30',
    'CP960': '73.80.0.35',
    'W52P': '25.80.0.15',
}
COMMON_FILES = [
    ('y000000000028.cfg', 'T46-28.80.0.95.rom', 'model.tpl'),
    ('y000000000029.cfg', 'T42-29.80.0.95.rom', 'model.tpl'),
    ('y000000000035.cfg', 'T48-35.80.0.95.rom', 'model.tpl'),
    ('y000000000036.cfg', 'T41-36.80.0.95.rom', 'model.tpl'),
    ('y000000000044.cfg', 'T23-44.80.0.95.rom', 'model.tpl'),
    ('y000000000045.cfg', 'T27-45.80.0.95.rom', 'model.tpl'),
    ('y000000000046.cfg', 'T29-46.80.0.95.rom', 'model.tpl'),
    ('y000000000051.cfg', 'T49-51.80.0.100.rom', 'model.tpl'),
    ('y000000000052.cfg', 'T21P_E2-52.80.0.95.rom', 'model.tpl'),
    ('y000000000053.cfg', 'T19P_E2-53.80.0.95.rom', 'model.tpl'),
    ('y000000000054.cfg', 'T40-54.80.0.95.rom', 'model.tpl'),
    ('y000000000037.cfg', 'CP860-37.80.0.30.rom', 'model.tpl'),
    ('y000000000073.cfg', 'CP960-73.80.0.35.rom', 'model.tpl'),
]

COMMON_FILES_DECT = [
    (
        'y000000000025.cfg',
        'Base for W52P&W56P-25.80.0.15.rom',
        'W56H-61.80.0.15.rom',
        'W52P.tpl',
    ),
]


class YealinkPlugin(common_globals['BaseYealinkPlugin']):
    IS_PLUGIN = True

    pg_associator = common_globals['BaseYealinkPgAssociator'](MODEL_VERSIONS)

    # Yealink plugin specific stuff

    _COMMON_FILES = COMMON_FILES

    def configure_common(self, raw_config):
        super().configure_common(raw_config)
        for (
            filename,
            fw_filename,
            fw_handset_filename,
            tpl_filename,
        ) in COMMON_FILES_DECT:
            tpl = self._tpl_helper.get_template(f'common/{tpl_filename}')
            dst = os.path.join(self._tftpboot_dir, filename)
            raw_config['XX_fw_filename'] = fw_filename
            raw_config['XX_fw_handset_filename'] = fw_handset_filename
            self._tpl_helper.dump(tpl, raw_config, dst, self._ENCODING)
