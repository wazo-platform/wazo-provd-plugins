"""
Copyright 2013-2022 The Wazo Authors  (see the AUTHORS file)
SPDX-License-Identifier: GPL-3.0-or-later

Depends on the following external programs:
 -rsync
"""

from subprocess import check_call


@target('v73', 'wazo-yealink-v73')
def build_v73(path):
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*', 'v73/', path])


@target('v80', 'wazo-yealink-v80')
def build_v80(path):
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*', 'v80/', path])


@target('v81', 'wazo-yealink-v81')
def build_v81(path):
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*', 'v81/', path])


@target('v82', 'wazo-yealink-v82')
def build_v82(path):
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*', 'v82/', path])


@target('v83', 'wazo-yealink-v83')
def build_v83(path):
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*', 'v83/', path])


@target('v84', 'wazo-yealink-v84')
def build_v84(path):
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*', 'v84/', path])


@target('v85', 'wazo-yealink-v85')
def build_v85(path):
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*', 'v85/', path])


@target('v86', 'wazo-yealink-v86')
def build_v86(path):
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*', 'v86/', path])
