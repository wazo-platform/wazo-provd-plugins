# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

# Depends on the following external programs:
#  -rsync

from subprocess import check_call


@target('N510', 'wazo-gigaset-N510')
def build_N510(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*',
                'N510/', path])


@target('N720', 'wazo-gigaset-N720')
def build_N720(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*',
                'N720/', path])


@target('N870', 'wazo-gigaset-N870-83.v2.17.2')
def build_N870_83_v2_17_2(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                'N870-83.v2.17.2/', path])
