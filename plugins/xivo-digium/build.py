# Copyright 2014-2022 The Wazo Authors  (see the AUTHORS file)
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

from subprocess import check_call


@target('1.4.0.0', 'xivo-digium-1.4.0.0')
def build_1_4_0_0(path):
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*', '1.4.0.0/', path])


@target('2.2.1.8', 'xivo-digium-2.2.1.8')
def build_2_2_1_8(path):
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*', '2.2.1.8/', path])


@target('2.8.1', 'wazo-digium-2.8.1')
def build_2_8_1(path):
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*', '2.8.1/', path])
