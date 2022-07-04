# -*- coding: utf-8 -*-
# Copyright 2014-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

# Depends on the following external programs:
#  -rsync

from subprocess import check_call


# target(<target_id>, <pg_id>)
# any error raised will be considered a build error
# Pre: pg_dir is initially empty
# Pre: current directory is the one of the bplugin
@target('3.3.1-SP4', 'xivo-aastra-3.3.1-SP4')
def build_3_3_1_sp4(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                '--exclude', '/templates/68*.tpl',
                'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*',
                '3.3.1-SP4/', path])


@target('4.3.0', 'xivo-aastra-4.3.0')
def build_4_3_0(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                '--exclude', '/templates/67*',
                '--exclude', '/templates/9*',
                'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*',
                '4.3.0/', path])


@target('4.2.0', 'wazo-aastra-4.2.0')
def build_4_2_0(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                '--exclude', '/templates/67*',
                '--exclude', '/templates/9*',
                'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*',
                '4.2.0/', path])


@target('5.0.0', 'wazo-aastra-5.0.0')
def build_5_0_0(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                '--exclude', '/templates/67*',
                '--exclude', '/templates/9*',
                'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*',
                '5.0.0/', path])


@target('5.1.0', 'wazo-aastra-5.1.0')
def build_5_1_0(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                '--exclude', '/templates/67*',
                '--exclude', '/templates/9*',
                '--exclude', '/templates/68*',
                'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*',
                '5.1.0/', path])
