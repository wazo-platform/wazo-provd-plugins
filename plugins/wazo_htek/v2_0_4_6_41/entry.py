# Copyright 2020-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

common_globals = {}
execfile_('common.py', common_globals)

MODEL_VERSIONS = {
    'UC926': '2.0.4.6.41',
    'UC924': '2.0.4.6.41',
    'UC923': '2.0.4.6.41',
    'UC912': '2.0.4.6.41',
    'UC912G': '2.0.4.6.41',
    'UC903': '2.0.4.6.41',
    'UC902': '2.0.4.6.41',
}

COMMON_FILES = [
    ('cfg0010.xml', 'model.tpl'),  # UC926
    ('cfg0012.xml', 'model.tpl'),  # UC924
    ('cfg0013.xml', 'model.tpl'),  # UC923
    ('cfg0016.xml', 'model.tpl'),  # UC903
    ('cfg0017.xml', 'model.tpl'),  # UC902
    ('cfg0019.xml', 'model.tpl'),  # UC912 / UC912G / UC912E
]


class HtekPlugin(common_globals['BaseHtekPlugin']):
    IS_PLUGIN = True

    pg_associator = common_globals['BaseHtekPgAssociator'](MODEL_VERSIONS)

    # Htek plugin specific stuff

    _COMMON_FILES = COMMON_FILES
