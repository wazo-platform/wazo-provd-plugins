# Copyright 2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

# Depends on the following external programs:
#  -rsync

from subprocess import check_call


@target('2.13.02', 'wazo-alcatel-2.13.02')
def build_2_13_02(path):
    check_call(['rsync', '-rlp', '--exclude', '.*', '2.13.02/', path])
