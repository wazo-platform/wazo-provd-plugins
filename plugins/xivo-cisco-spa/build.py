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


@target('7.5.5', 'xivo-cisco-spa-7.5.5')
def build_7_5_5(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                'common/', path])
    
    check_call(['rsync', '-rlp', '--exclude', '.*',
                '7.5.5/', path])


@target('legacy', 'xivo-cisco-spa-legacy')
def build_legacy(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                'common/', path])
    
    check_call(['rsync', '-rlp', '--exclude', '.*',
                'legacy/', path])


@target('pap2t-5.1.6', 'xivo-cisco-pap2t-5.1.6')
def build_pap2t_5_1_6(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                'common/', path])
    
    check_call(['rsync', '-rlp', '--exclude', '.*',
                'pap2t-5.1.6/', path])


@target('spa2102-5.2.12', 'xivo-cisco-spa2102-5.2.12')
def build_spa2102_5_2_12(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                'common/', path])
    
    check_call(['rsync', '-rlp', '--exclude', '.*',
                'spa2102-5.2.12/', path])


@target('spa3102-5.1.10', 'xivo-cisco-spa3102-5.1.10')
def build_spa3102_5_1_10(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                'common/', path])
    
    check_call(['rsync', '-rlp', '--exclude', '.*',
                'spa3102-5.1.10/', path])


@target('spa8000-6.1.11', 'xivo-cisco-spa8000-6.1.11')
def build_spa8000_6_1_11(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                'common/', path])
    
    check_call(['rsync', '-rlp', '--exclude', '.*',
                'spa8000-6.1.11/', path])


@target('spa8800-6.1.7', 'xivo-cisco-spa8800-6.1.7')
def build_spa8800_6_1_7(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                'common/', path])
    
    check_call(['rsync', '-rlp', '--exclude', '.*',
                'spa8800-6.1.7/', path])
