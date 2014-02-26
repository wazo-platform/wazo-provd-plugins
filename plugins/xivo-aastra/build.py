# -*- coding: utf-8 -*-

# Copyright (C) 2014 Avencall
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


# target(<target_id>, <pg_id>)
# any error raised will be considered a build error
# Pre: pg_dir is initially empty
# Pre: current directory is the one of the bplugin
@target('3.2.2-SP3', 'xivo-aastra-3.2.2-SP3')
def build_3_2_2_sp3(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                '--exclude', '/templates/6751i.tpl',
                'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*',
                '3.2.2-SP3/', path])


@target('3.3.1-SP2', 'xivo-aastra-3.3.1-SP2')
def build_3_3_1_sp2(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                '--exclude', '/templates/6751i.tpl',
                'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*',
                '3.3.1-SP2/', path])


@target('switchboard', 'xivo-aastra-switchboard')
def build_switchboard(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                '--include', '/templates/6731i.tpl',
                '--include', '/templates/6755i.tpl',
                '--include', '/templates/6757i.tpl',
                '--include', '/templates/base.tpl',
                '--exclude', '/templates/*',
                'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*',
                'switchboard/', path])
