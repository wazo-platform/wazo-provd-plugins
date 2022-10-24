# Copyright 2013-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

common_globals = {}
execfile_('common.py', common_globals)

MODEL_VERSIONS = {
    'CP920': '78.84.0.125',
    'CP960': '73.84.0.25',
    'T19P_E2': '53.84.0.125',  # >=53.84.0.90 version does not support YDMP and YMCS
    'T21P_E2': '52.84.0.125',  # >=52.84.0.90 version does not support YDMP and YMCS
    'T23P': '44.84.0.140',  # >=44.84.0.90 version does not support YDMP and YMCS
    'T23G': '44.84.0.140',  # >=44.84.0.90 version does not support YDMP and YMCS
    'T27G': '69.84.0.125',
    'T40P': '54.84.0.125',  # >=54.84.0.90 version does not support YDMP and YMCS
    'T40G': '76.84.0.125',  # >=76.84.0.90 version does not support YDMP and YMCS
    'T41S': '66.84.0.125',
    'T42S': '66.84.0.125',
    'T46S': '66.84.0.125',
    'T48S': '66.84.0.125',
    'T52S': '70.84.0.70',
    'T53': '95.84.0.125',
    'T53W': '95.84.0.125',
    'T54S': '70.84.0.70',
    'T54W': '96.84.0.125',
    'T57W': '97.84.0.125',
    'T58': '58.84.0.25',
}

COMMON_FILES = [
    ('y000000000044.cfg', 'T23-44.84.0.140.rom', 'model.tpl'),
    ('y000000000069.cfg', 'T27G-69.84.0.125.rom', 'model.tpl'),
    ('y000000000052.cfg', 'T21P_E2-52.84.0.125.rom', 'model.tpl'),
    ('y000000000053.cfg', 'T19P_E2-53.84.0.125.rom', 'model.tpl'),
    ('y000000000054.cfg', 'T40-54.84.0.125.rom', 'model.tpl'),
    ('y000000000076.cfg', 'T40G-76.84.0.125.rom', 'model.tpl'),
    ('y000000000065.cfg', 'T46S(T48S,T42S,T41S)-66.84.0.125.rom', 'model.tpl'),
    ('y000000000066.cfg', 'T46S(T48S,T42S,T41S)-66.84.0.125.rom', 'model.tpl'),
    ('y000000000067.cfg', 'T46S(T48S,T42S,T41S)-66.84.0.125.rom', 'model.tpl'),
    ('y000000000068.cfg', 'T46S(T48S,T42S,T41S)-66.84.0.125.rom', 'model.tpl'),
    ('y000000000095.cfg', 'T53W(T53)-95.84.0.125.rom', 'model.tpl'),
    ('y000000000070.cfg', 'T54S(T52S)-70.84.0.70.rom', 'model.tpl'),
    ('y000000000096.cfg', 'T54W-96.84.0.125.rom', 'model.tpl'),
    ('y000000000097.cfg', 'T57W-97.84.0.125.rom', 'model.tpl'),
    ('y000000000058.cfg', 'T58-58.84.0.25.rom', 'model.tpl'),
    ('y000000000078.cfg', 'CP920-78.84.0.125.rom', 'model.tpl'),
    ('y000000000073.cfg', 'CP960-73.84.0.25.rom', 'model.tpl'),
]


class YealinkPlugin(common_globals['BaseYealinkPlugin']):
    IS_PLUGIN = True

    pg_associator = common_globals['BaseYealinkPgAssociator'](MODEL_VERSIONS)

    # Yealink plugin specific stuff

    _COMMON_FILES = COMMON_FILES
