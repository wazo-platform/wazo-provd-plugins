# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

common = {}
execfile_('common.py', common)


MODEL_VERSIONS = {
    'N510 IP PRO': '42.262.00.000.000',
}


class GigasetPlugin(common['BaseGigasetPlugin']):
    IS_PLUGIN = True

    pg_associator = common['BaseGigasetPgAssociator'](MODEL_VERSIONS)