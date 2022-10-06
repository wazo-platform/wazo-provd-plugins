# -*- coding: utf-8 -*-
# Copyright 2013-2021 The Wazo Authors  (see the AUTHORS file)
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


@target('N870-83.v2.39.0', 'wazo-gigaset-N870-83.v2.39.0')
def build_N870_83_v2_39_0(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                'N870-83.v2.39.0/', path])


@target('N870-83.v2.48.0', 'wazo-gigaset-N870-83.v2.48.0')
def build_N870_83_v2_48_0(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                'N870-83.v2.48.0/', path])

@target('Nx70-83.v2.49.1', 'wazo-gigaset-Nx70-83.v2.49.1')
def build_Nx70_83_v2_48_0(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                'Nx70-83.v2.49.1/', path])
