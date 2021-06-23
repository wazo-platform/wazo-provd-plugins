# -*- coding: utf-8 -*-

# Copyright 2013-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import os

common_globals = {}
execfile_('common.py', common_globals)

MODEL_VERSIONS = {
    u'T19P_E2': u'53.82.0.20',
    u'T21P_E2': u'52.82.0.20',
    u'T23P': u'44.82.0.20',
    u'T23G': u'44.82.0.20',
    u'T27P': u'45.82.0.30',
    u'T27G': u'69.82.0.30',
    u'T29G': u'46.82.0.30',
    u'T40P': u'54.82.0.20',
    u'T40G': u'76.82.0.20',
    u'T41P': u'36.82.0.20',
    u'T41S': u'66.82.0.30',
    u'T42G': u'29.82.0.20',
    u'T42S': u'66.82.0.30',
    u'T46G': u'28.82.0.30',
    u'T46S': u'66.82.0.30',
    u'T48G': u'35.82.0.30',
    u'T48S': u'66.82.0.30',
}

COMMON_FILES = [
    ('y000000000028.cfg', u'T46-28.82.0.30.rom', 'model.tpl'),
    ('y000000000029.cfg', u'T42-29.82.0.20.rom', 'model.tpl'),
    ('y000000000035.cfg', u'T48-35.82.0.30.rom', 'model.tpl'),
    ('y000000000036.cfg', u'T41-36.82.0.20.rom', 'model.tpl'),
    ('y000000000044.cfg', u'T23-44.82.0.20.rom', 'model.tpl'),
    ('y000000000045.cfg', u'T27-45.82.0.30.rom', 'model.tpl'),
    ('y000000000069.cfg', u'T27G-69.82.0.30.rom', 'model.tpl'),
    ('y000000000046.cfg', u'T29-46.82.0.30.rom', 'model.tpl'),
    ('y000000000052.cfg', u'T21P_E2-52.82.0.20.rom', 'model.tpl'),
    ('y000000000053.cfg', u'T19P_E2-53.82.0.20.rom', 'model.tpl'),
    ('y000000000054.cfg', u'T40-54.82.0.20.rom', 'model.tpl'),
    ('y000000000076.cfg', u'T40G-76.82.0.20.rom', 'model.tpl'),
    ('y000000000066.cfg', u'T46S(T48S,T42S,T41S)-66.82.0.30.rom', 'model.tpl'),
]


class YealinkPlugin(common_globals['BaseYealinkPlugin']):
    IS_PLUGIN = True

    pg_associator = common_globals['BaseYealinkPgAssociator'](MODEL_VERSIONS)

    # Yealink plugin specific stuff

    _COMMON_FILES = COMMON_FILES
