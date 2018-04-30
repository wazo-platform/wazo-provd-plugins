# -*- coding: utf-8 -*-

# Copyright 2010-2018 The Wazo Authors  (see the AUTHORS file)
# Contributor: Sébastien Le Moal <sebastien.calexium.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

common = {}
execfile_('common.py', common)

MODELS = [
    u'X2',
    u'X3',
    u'X3S',
    u'X4',
    u'X5',
    u'X5S',
    u'X6',
    u'X6V2'
]

COMMON_FILES = [
    ('F0V00X200000.cfg', u'x2R2.2.0.3753T20170803142949.z', 'model.tpl'),
    ('F0V00X300000.cfg', u'x31.4.0.2016T20170303152729.z', 'model.tpl'),
    ('f0X3shw1.100.cfg', u'x3s2.4.0.5487T20180309151655.z', 'model.tpl'),
    ('f0X4hw1.100.cfg', u'x42.4.0.5487T20180309151511.z', 'model.tpl'),
    ('f0X5hw1.100.cfg', u'x51.4.0.2016T20170303151233.z', 'model.tpl'),
    ('F0V00X5S0000.cfg', u'x5s-6900-P0.11.7-1.4.1-2303T2018-03-14-16.01.18.z', 'model.tpl'),
    ('F0V00X600000.cfg', u'x6-6904-P0.11.7-1.4.1-2303T2018-03-14-15.21.29.z', 'model.tpl'),
    ('F0000X600000.cfg', u'x6-6914-P0.11.7-1.4.1-2303T2018-03-14-17.46.14.z', 'model.tpl'),
]


class FanvilPlugin(common['BaseFanvilPlugin']):
    IS_PLUGIN = True

    _COMMON_FILES = COMMON_FILES

    pg_associator = common['BaseFanvilPgAssociator'](MODELS)
