# -*- coding: utf-8 -*-

# Copyright 2017-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

# Depends on the following external programs:
#  -rsync

from subprocess import check_call

@target('2.0.4.4.58', 'wazo-htek-2.0.4.4.58')
def build_2_0_4_4_58(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*',
                '2.0.4.4.58/', path])

@target('2.0.4.6.41', 'wazo-htek-2.0.4.6.41')
def build_2_0_4_6_41(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*',
                '2.0.4.6.41/', path])
