"""
Copyright 2013-2023 The Wazo Authors  (see the AUTHORS file)
SPDX-License-Identifier: GPL-3.0-or-later

Depends on the following external programs:
 -rsync
"""

from subprocess import check_call


@target('2.3', 'wazo-fanvil-2.3')
def build_2_3(path):
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*', '2.3/', path])


@target('serie-x', 'wazo-fanvil-serie-x')
def build_x(path):
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*', 'serie-x/', path])


@target('serie-v', 'wazo-fanvil-serie-v')
def build_v(path):
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*', 'serie-v/', path])
