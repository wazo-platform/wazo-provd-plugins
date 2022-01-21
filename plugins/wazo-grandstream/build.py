# -*- coding: utf-8 -*-

# Copyright 2013-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

# Depends on the following external programs:
#  -rsync

from subprocess import check_call


@target('1.0.27.2', 'wazo-grandstream-1.0.27.2')
def build_1_0_27_2(path):
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/*',
            'common_ata/',
            path,
        ]
    )

    check_call(['rsync', '-rlp', '--exclude', '.*', '1.0.27.2/', path])


@target('1.0.3.27', 'wazo-grandstream-1.0.3.27')
def build_1_0_3_27(path):
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/*',
            'common/',
            path,
        ]
    )

    check_call(['rsync', '-rlp', '--exclude', '.*', '1.0.3.27/', path])


@target('1.0.3.2x-android', 'wazo-grandstream-1.0.3.2x-android')
def build_1_0_3_2x_android(path):
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/*',
            'common/',
            path,
        ]
    )

    check_call(['rsync', '-rlp', '--exclude', '.*', '1.0.3.2x-android/', path])


@target('1.0.5.48', 'wazo-grandstream-1.0.5.48')
def build_1_0_5_48(path):
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/*',
            'common/',
            path,
        ]
    )

    check_call(['rsync', '-rlp', '--exclude', '.*', '1.0.5.48/', path])


@target('1.0.7.13', 'wazo-grandstream-1.0.7.13')
def build_1_0_7_13(path):
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/*',
            'common/',
            path,
        ]
    )

    check_call(['rsync', '-rlp', '--exclude', '.*', '1.0.7.13/', path])


@target('1.0.8.6', 'wazo-grandstream-1.0.8.6')
def build_1_0_8_6(path):
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/*',
            'common/',
            path,
        ]
    )

    check_call(['rsync', '-rlp', '--exclude', '.*', '1.0.8.6/', path])


@target('1.0.8.9', 'wazo-grandstream-1.0.8.9')
def build_1_0_8_9(path):
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/*',
            'common/',
            path,
        ]
    )

    check_call(['rsync', '-rlp', '--exclude', '.*', '1.0.8.9/', path])


@target('1.2.5.3', 'wazo-grandstream-1.2.5.3')
def build_1_2_5_3(path):
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/*',
            'common/',
            path,
        ]
    )

    check_call(['rsync', '-rlp', '--exclude', '.*', '1.2.5.3/', path])
