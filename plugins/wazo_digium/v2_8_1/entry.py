# Copyright 2014-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

common = {}
execfile_('common.py', common)


VERSION = '2.8.1'


class DigiumPlugin(common['BaseDigiumPlugin']):
    IS_PLUGIN = True

    pg_associator = common['DigiumPgAssociator'](VERSION)
