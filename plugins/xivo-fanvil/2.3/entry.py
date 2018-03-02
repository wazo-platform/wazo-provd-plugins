# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
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
    u'C58',
    u'C62',
    u'X2',
    u'X3',
    u'X3S',
    u'X4',
    u'X5',
    u'X5S',
    u'X6'
]
COMMON_FILES = [
    ('f0C00580000.cfg', u'2c12MIMGV2_5_686_84T20170215103440.z', 'model.tpl'),
    ('f0C00620000.cfg', u'2c10MIMGV2_5_787_97T20170616102925.z', 'model.tpl'),
    ('F0V00X200000.cfg', u'x22.3.2.4638T20171221091842.z', 'model.tpl'),
    ('F0V00X300000.cfg', u'x31.4.0.2016T20170303152729.z', 'model.tpl'),
    ('f0X3shw1.100.cfg', u'x3s2.3.2.4638T20171221090439.z', 'model.tpl'),
    ('f0X4hw1.100.cfg', u'x42.3.2.4638T20171221091314.z', 'model.tpl'),
    ('f0X5hw1.100.cfg', u'x51.4.0.2016T20170303151233.z', 'model.tpl'),
    ('F0V0X5S00000.cfg', u'x5s-6900-P0.10.4-1.2.4-2146T2017-12-12-15.21.01.z', 'model.tpl'),
    ('F0V0X6000000.cfg', u'x6-6914-P0.10.4-1.2.4-2142T2017-12-11-19.13.38.z', 'model.tpl'),
]


class FanvilPlugin(common['BaseFanvilPlugin']):
    IS_PLUGIN = True

    _COMMON_FILES = COMMON_FILES

    pg_associator = common['BaseFanvilPgAssociator'](MODELS)
