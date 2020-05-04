# -*- coding: utf-8 -*-

# Copyright 2017-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import os

common_globals = {}
execfile_('common.py', common_globals)

MODEL_VERSIONS = {
    u'UC926': u'2.0.4.4.58',
    u'UC926E': u'2.0.4.4.58',
    u'UC924': u'2.0.4.4.58',
    u'UC924E': u'2.0.4.4.58',
    u'UC923': u'2.0.4.4.58',
    u'UC912': u'2.0.4.4.58',
    u'UC912E': u'2.0.4.4.58',
    u'UC912G': u'2.0.4.4.58',
    u'UC903': u'2.0.4.4.58',
    u'UC902': u'2.0.4.4.58',
    u'UC862': u'2.0.4.4.58',
    u'UC860': u'2.0.4.4.58',
    u'UC860P': u'2.0.4.4.58',
    u'UC842': u'2.0.4.4.58',
    u'UC840': u'2.0.4.4.58',
    u'UC840P': u'2.0.4.4.58',
    u'UC806': u'2.0.4.4.58',
    u'UC806T': u'2.0.4.4.58',
    u'UC804': u'2.0.4.4.58',
    u'UC804T': u'2.0.4.4.58',
    u'UC803': u'2.0.4.4.58',
    u'UC803T': u'2.0.4.4.58',
    u'UC802': u'2.0.4.4.58',
    u'UC802T': u'2.0.4.4.58',
}

COMMON_FILES = [
    ('cfg0000.xml', 'model.tpl'),  # UC862
    ('cfg0001.xml', 'model.tpl'),  # UC842
    ('cfg0002.xml', 'model.tpl'),  # UC860
    ('cfg0003.xml', 'model.tpl'),  # UC840
    ('cfg0004.xml', 'model.tpl'),  # UC806
    ('cfg0041.xml', 'model.tpl'),  # UC806T
    ('cfg0042.xml', 'model.tpl'),  # UC806G
    ('cfg0005.xml', 'model.tpl'),  # UC804
    ('cfg0051.xml', 'model.tpl'),  # UC804T
    ('cfg0052.xml', 'model.tpl'),  # UC804G
    ('cfg0006.xml', 'model.tpl'),  # UC803 / UC803T
    ('cfg0007.xml', 'model.tpl'),  # UC802 / UC802T
    ('cfg0010.xml', 'model.tpl'),  # UC926
    ('cfg0110.xml', 'model.tpl'),  # UC926E
    ('cfg0012.xml', 'model.tpl'),  # UC924
    ('cfg0112.xml', 'model.tpl'),  # UC924E
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
