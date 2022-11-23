# Copyright 2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

# Depends on the following external programs:
#  -rsync

from subprocess import check_call


@target('2.01.10', 'wazo-alcatel-2.01.10')
def build_2_01_10(path):
    check_call(['rsync', '-rlp', '--exclude', '.*', '2.01.10/', path])


@target('2.13.02', 'wazo-alcatel-2.13.02')
def build_2_13_02(path):
<<<<<<< HEAD
    check_call(['rsync', '-rlp', '--exclude', '.*', '2.13.02/', path])
=======
    check_call(
        ['rsync', '-rlp', '--exclude', '.*', '2.13.02/', path]
    )

@target('1.51.52', 'wazo-alcatel-1.51.52')
def build_1_55_03(path):
    check_call(
        ['rsync', '-rlp', '--exclude', '.*', '1.51.52/', path]
    )
>>>>>>> first release
