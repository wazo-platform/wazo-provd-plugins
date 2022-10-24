# Copyright 2013-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import os

common_globals = {}
execfile_('common.py', common_globals)

MODEL_VERSIONS = {
    'T19P_E2': '53.82.0.20',
    'T21P_E2': '52.82.0.20',
    'T23P': '44.82.0.20',
    'T23G': '44.82.0.20',
    'T27P': '45.82.0.30',
    'T27G': '69.82.0.30',
    'T29G': '46.82.0.30',
    'T40P': '54.82.0.20',
    'T40G': '76.82.0.20',
    'T41P': '36.82.0.20',
    'T41S': '66.82.0.30',
    'T42G': '29.82.0.20',
    'T42S': '66.82.0.30',
    'T46G': '28.82.0.30',
    'T46S': '66.82.0.30',
    'T48G': '35.82.0.30',
    'T48S': '66.82.0.30',
}

COMMON_FILES = [
    ('y000000000028.cfg', 'T46-28.82.0.30.rom', 'model.tpl'),
    ('y000000000029.cfg', 'T42-29.82.0.20.rom', 'model.tpl'),
    ('y000000000035.cfg', 'T48-35.82.0.30.rom', 'model.tpl'),
    ('y000000000036.cfg', 'T41-36.82.0.20.rom', 'model.tpl'),
    ('y000000000044.cfg', 'T23-44.82.0.20.rom', 'model.tpl'),
    ('y000000000045.cfg', 'T27-45.82.0.30.rom', 'model.tpl'),
    ('y000000000069.cfg', 'T27G-69.82.0.30.rom', 'model.tpl'),
    ('y000000000046.cfg', 'T29-46.82.0.30.rom', 'model.tpl'),
    ('y000000000052.cfg', 'T21P_E2-52.82.0.20.rom', 'model.tpl'),
    ('y000000000053.cfg', 'T19P_E2-53.82.0.20.rom', 'model.tpl'),
    ('y000000000054.cfg', 'T40-54.82.0.20.rom', 'model.tpl'),
    ('y000000000076.cfg', 'T40G-76.82.0.20.rom', 'model.tpl'),
    ('y000000000066.cfg', 'T46S(T48S,T42S,T41S)-66.82.0.30.rom', 'model.tpl'),
]


class YealinkPlugin(common_globals['BaseYealinkPlugin']):
    IS_PLUGIN = True

    pg_associator = common_globals['BaseYealinkPgAssociator'](MODEL_VERSIONS)

    # Yealink plugin specific stuff

    _COMMON_FILES = COMMON_FILES
