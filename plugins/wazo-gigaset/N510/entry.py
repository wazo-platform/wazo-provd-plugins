# -*- coding: utf-8 -*-
# Copyright 2017-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

common = {}
execfile_('common.py', common)


MODEL_VERSIONS = {
    u'N510 IP PRO': u'42.258',
}


class GigasetPlugin(common['BaseGigasetPlugin']):
    IS_PLUGIN = True

    pg_associator = common['BaseGigasetPgAssociator'](MODEL_VERSIONS)
