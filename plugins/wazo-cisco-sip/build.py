# -*- coding: utf-8 -*-

# Copyright 2018-2020 The Wazo Authors (see AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

# Depends on the following external programs:
#  -rsync

from subprocess import check_call


@target('9.3', 'wazo-cisco-sip-9.3')
def build_9_3(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*',
                '9.3/', path])


@target('11.1.0', 'wazo-cisco-sip-11.1.0')
def build_11_3_1(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                '11.1.0/', path])


@target('11.3.1', 'wazo-cisco-sip-11.3.1')
def build_11_3_1(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                '11.3.1/', path])
