# Copyright (C) 2013-2022 The Wazo Authors  (see the AUTHORS file)
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


@target('ST2022-4.78.1', 'wazo-technicolor-ST2022-4.78.1')
def build_ST2022_4_78_1(path):
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/base.tpl',
            '--include',
            '/templates/ST2022.tpl',
            '--exclude',
            '/templates/*',
            'common/',
            path,
        ]
    )

    check_call(['rsync', '-rlp', '--exclude', '.*', 'ST2022-4.78.1/', path])


@target('ST2030-2.74', 'wazo-technicolor-ST2030-2.74')
def build_ST2030_2_74(path):
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/base.tpl',
            '--include',
            '/templates/ST2030.tpl',
            '--exclude',
            '/templates/*',
            'common/',
            path,
        ]
    )

    check_call(['rsync', '-rlp', '--exclude', '.*', 'ST2030-2.74/', path])


@target('TB30-1.74.0', 'wazo-technicolor-TB30-1.74.0')
def build_TB30_1_74_0(path):
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/base.tpl',
            '--include',
            '/templates/TB30.tpl',
            '--exclude',
            '/templates/*',
            'common/',
            path,
        ]
    )

    check_call(['rsync', '-rlp', '--exclude', '.*', 'TB30-1.74.0/', path])
