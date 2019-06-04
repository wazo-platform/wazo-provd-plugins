# -*- coding: utf-8 -*-
# Copyright 2015-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

common = {}
execfile_('common.py', common)


MODEL_VERSIONS = {
    u'6863i': u'4.2.0.2023',
    u'6865i': u'4.2.0.2023',
    u'6867i': u'4.2.0.2023',
    u'6869i': u'4.2.0.2023',
}


class AastraPlugin(common['BaseAastraPlugin']):
    IS_PLUGIN = True
    _LANGUAGE_PATH = 'Aastra/i18n/'

    pg_associator = common['BaseAastraPgAssociator'](MODEL_VERSIONS)
