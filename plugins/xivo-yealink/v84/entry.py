# -*- coding: utf-8 -*-

# Copyright 2013-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

common_globals = {}
execfile_('common.py', common_globals)

MODEL_VERSIONS = {
    u'CP920': u'78.84.0.125',
    u'CP960': u'73.84.0.25',
    u'T19P_E2': u'53.84.0.125',  # >=53.84.0.90 version does not support YDMP and YMCS
    u'T21P_E2': u'52.84.0.125',  # >=52.84.0.90 version does not support YDMP and YMCS
    u'T23P': u'44.84.0.140',  # >=44.84.0.90 version does not support YDMP and YMCS
    u'T23G': u'44.84.0.140',  # >=44.84.0.90 version does not support YDMP and YMCS
    u'T27G': u'69.84.0.125',
    u'T40P': u'54.84.0.125',  # >=54.84.0.90 version does not support YDMP and YMCS
    u'T40G': u'76.84.0.125',  # >=76.84.0.90 version does not support YDMP and YMCS
    u'T41S': u'66.84.0.125',
    u'T42S': u'66.84.0.125',
    u'T46S': u'66.84.0.125',
    u'T48S': u'66.84.0.125',
    u'T52S': u'70.84.0.70',
    u'T53': u'95.84.0.125',
    u'T53W': u'95.84.0.125',
    u'T54S': u'70.84.0.70',
    u'T54W': u'96.84.0.125',
    u'T57W': u'97.84.0.125',
    u'T58': u'58.84.0.25',
}

COMMON_FILES = [
    ('y000000000044.cfg', u'T23-44.84.0.140.rom', 'model.tpl'),
    ('y000000000069.cfg', u'T27G-69.84.0.125.rom', 'model.tpl'),
    ('y000000000052.cfg', u'T21P_E2-52.84.0.125.rom', 'model.tpl'),
    ('y000000000053.cfg', u'T19P_E2-53.84.0.125.rom', 'model.tpl'),
    ('y000000000054.cfg', u'T40-54.84.0.125.rom', 'model.tpl'),
    ('y000000000076.cfg', u'T40G-76.84.0.125.rom', 'model.tpl'),
    ('y000000000065.cfg', u'T46S(T48S,T42S,T41S)-66.84.0.125.rom', 'model.tpl'),
    ('y000000000066.cfg', u'T46S(T48S,T42S,T41S)-66.84.0.125.rom', 'model.tpl'),
    ('y000000000067.cfg', u'T46S(T48S,T42S,T41S)-66.84.0.125.rom', 'model.tpl'),
    ('y000000000068.cfg', u'T46S(T48S,T42S,T41S)-66.84.0.125.rom', 'model.tpl'),
    ('y000000000095.cfg', u'T53W(T53)-95.84.0.125.rom', 'model.tpl'),
    ('y000000000070.cfg', u'T54S(T52S)-70.84.0.70.rom', 'model.tpl'),
    ('y000000000096.cfg', u'T54W-96.84.0.125.rom', 'model.tpl'),
    ('y000000000097.cfg', u'T57W-97.84.0.125.rom', 'model.tpl'),
    ('y000000000058.cfg', u'T58-58.84.0.25.rom', 'model.tpl'),
    ('y000000000078.cfg', u'CP920-78.84.0.125.rom', 'model.tpl'),
    ('y000000000073.cfg', u'CP960-73.84.0.25.rom', 'model.tpl'),
]


class YealinkPlugin(common_globals['BaseYealinkPlugin']):
    IS_PLUGIN = True

    pg_associator = common_globals['BaseYealinkPgAssociator'](MODEL_VERSIONS)

    # Yealink plugin specific stuff

    _COMMON_FILES = COMMON_FILES
