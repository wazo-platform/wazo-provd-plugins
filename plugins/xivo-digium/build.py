# -*- coding: UTF-8 -*-

from subprocess import check_call


@target('1.1.0.0', 'xivo-digium-1.1.0.0')
def build_1_1_0_0(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*',
                '1.1.0.0/', path])
