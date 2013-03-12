# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
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

import os.path
from subprocess import check_call


@target('sccp-8.5.2', 'xivo-cisco-sccp-8.5.2')
def build_sccp_8_5_2(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                'common/', path])
    
    check_call(['rsync', '-rlp', '--exclude', '.*',
                'sccp-common/', path])
    
    check_call(['rsync', '-rlp', '--exclude', '.*',
                'sccp-8.5.2/', path])


@target('sccp-9.0.3', 'xivo-cisco-sccp-9.0.3')
def build_sccp_9_0_3(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*',
                'sccp-common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*',
                'sccp-9.0.3/', path])


@target('sccp-9.2.1', 'xivo-cisco-sccp-9.2.1')
def build_sccp_9_2_1(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                'common/', path])
    
    check_call(['rsync', '-rlp', '--exclude', '.*',
                'sccp-common/', path])
    
    check_call(['rsync', '-rlp', '--exclude', '.*',
                'sccp-9.2.1/', path])


@target('sccp-legacy', 'xivo-cisco-sccp-legacy')
def build_sccp_legacy(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                'common/', path])
    
    check_call(['rsync', '-rlp', '--exclude', '.*',
                'sccp-common/', path])
    
    check_call(['rsync', '-rlp', '--exclude', '.*',
                'sccp-legacy/', path])


@target('sip-9.2.1', 'xivo-cisco-sip-9.2.1')
def build_sip_9_2_1(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                'common/', path])
    
    check_call(['rsync', '-rlp', '--exclude', '.*',
                'sip-common/', path])
    
    check_call(['rsync', '-rlp', '--exclude', '.*',
                'sip-9.2.1/', path])
