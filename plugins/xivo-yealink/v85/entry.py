# -*- coding: utf-8 -*-

# Copyright 2013-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

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
}

COMMON_FILES = [
    ('y0000000000123.cfg', u'T31(T30,T30P,T31G,T31P,T33P,T33G)-124.85.0.15.rom', 'model.tpl'),
    ('y0000000000124.cfg', u'T31(T30,T30P,T31G,T31P,T33P,T33G)-124.85.0.15.rom', 'model.tpl'),
    ('y0000000000127.cfg', u'T31(T30,T30P,T31G,T31P,T33P,T33G)-124.85.0.15.rom', 'model.tpl'),
]


class YealinkPlugin(common_globals['BaseYealinkPlugin']):
    IS_PLUGIN = True

    pg_associator = common_globals['BaseYealinkPgAssociator'](MODEL_VERSIONS)

    # Yealink plugin specific stuff

    _COMMON_FILES = COMMON_FILES
