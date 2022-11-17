# Copyright 2015-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

common = {}
execfile_('common.py', common)


MODEL_VERSIONS = {
    '6863i': '4.2.0.2023',
    '6865i': '4.2.0.2023',
    '6867i': '4.2.0.2023',
    '6869i': '4.2.0.2023',
}


class AastraPlugin(common['BaseAastraPlugin']):
    IS_PLUGIN = True
    _LANGUAGE_PATH = 'Aastra/i18n/'

    pg_associator = common['BaseAastraPgAssociator'](MODEL_VERSIONS)
