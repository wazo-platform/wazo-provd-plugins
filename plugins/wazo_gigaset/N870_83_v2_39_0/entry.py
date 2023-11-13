# Copyright 2017-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

common = {}
execfile_('common.py', common)


MODEL_VERSIONS = {
    'N870 IP PRO': '83.V2.39.0',
}


class GigasetPlugin(common['BaseGigasetPlugin']):
    IS_PLUGIN = True

    pg_associator = common['BaseGigasetPgAssociator'](MODEL_VERSIONS)
