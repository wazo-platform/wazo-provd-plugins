# -*- coding: utf-8 -*-

# Copyright 2014-2017 The Wazo Authors  (see the AUTHORS file)
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

# Depends on the following external programs:
#  -rsync

from subprocess import check_call


@target('4.0.11', 'xivo-polycom-4.0.11')
def build_4_0_11(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                '--include', '/templates/base.tpl',
                '--include', '/templates/SPIP321.tpl',
                '--include', '/templates/SPIP331.tpl',
                '--include', '/templates/SPIP335.tpl',
                '--include', '/templates/SPIP450.tpl',
                '--include', '/templates/SPIP550.tpl',
                '--include', '/templates/SPIP560.tpl',
                '--include', '/templates/SPIP650.tpl',
                '--include', '/templates/SPIP670.tpl',
                '--include', '/templates/SSIP5000.tpl',
                '--include', '/templates/SSIP6000.tpl',
                '--include', '/templates/SSIP7000.tpl',
                '--exclude', '/templates/*',
                'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*',
                '4.0.11/', path])


@target('5.4.3', 'xivo-polycom-5.4.3')
def build_5_4_3(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                '--include', '/templates/base.tpl',
                '--include', '/templates/VVX101.tpl',
                '--include', '/templates/VVX201.tpl',
                '--include', '/templates/VVX300.tpl',
                '--include', '/templates/VVX310.tpl',
                '--include', '/templates/VVX400.tpl',
                '--include', '/templates/VVX410.tpl',
                '--include', '/templates/VVX500.tpl',
                '--include', '/templates/VVX600.tpl',
                '--include', '/templates/VVX1500.tpl',
                '--exclude', '/templates/*',
                'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*',
                '5.4.3/', path])


@target('5.5.1', 'xivo-polycom-5.5.1')
def build_5_5_1(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                '--include', '/templates/base.tpl',
                '--include', '/templates/VVX101.tpl',
                '--include', '/templates/VVX201.tpl',
                '--include', '/templates/VVX300.tpl',
                '--include', '/templates/VVX310.tpl',
                '--include', '/templates/VVX400.tpl',
                '--include', '/templates/VVX410.tpl',
                '--include', '/templates/VVX500.tpl',
                '--include', '/templates/VVX600.tpl',
                '--include', '/templates/VVX1500.tpl',
                '--exclude', '/templates/*',
                'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*',
                '5.5.1/', path])


@target('3.2.4B', 'xivo-polycom-3.2.4B')
def build_3_2_4B(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                '--include', '/templates/base.tpl',
                '--include', '/templates/SPIP320.tpl',
                '--include', '/templates/SPIP321.tpl',
                '--include', '/templates/SPIP330.tpl',
                '--include', '/templates/SPIP331.tpl',
                '--include', '/templates/SPIP335.tpl',
                '--include', '/templates/SPIP430.tpl',
                '--include', '/templates/SPIP450.tpl',
                '--include', '/templates/SPIP550.tpl',
                '--include', '/templates/SPIP560.tpl',
                '--include', '/templates/SPIP650.tpl',
                '--include', '/templates/SPIP670.tpl',
                '--include', '/templates/SSIP5000.tpl',
                '--include', '/templates/SSIP6000.tpl',
                '--include', '/templates/SSIP7000.tpl',
                '--exclude', '/templates/*',
                'common-v3/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*',
                '3.2.4B/', path])


@target('3.1.6', 'xivo-polycom-3.1.6')
def build_3_1_6(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                '--include', '/templates/base.tpl',
                '--include', '/templates/SPIP301.tpl',
                '--include', '/templates/SPIP501.tpl',
                '--include', '/templates/SPIP600.tpl',
                '--include', '/templates/SPIP601.tpl',
                '--include', '/templates/SSIP4000.tpl',
                '--exclude', '/templates/*',
                'common-v3/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*',
                '3.1.6/', path])
