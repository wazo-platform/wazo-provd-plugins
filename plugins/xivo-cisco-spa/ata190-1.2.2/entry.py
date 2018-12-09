# -*- coding: utf-8 -*-

# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

common = {}
execfile_('common.py', common)

MODEL_VERSION = {u'ATA190': u'1.2.2'}


class CiscoPlugin(common['BaseCiscoPlugin']):
    IS_PLUGIN = True
    _COMMON_FILENAMES = ['dialplan.xml']
    pg_associator = common['BaseCiscoPgAssociator'](MODEL_VERSION)
