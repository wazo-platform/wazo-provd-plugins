# -*- coding: UTF-8 -*-

# Depends on the following external programs:
#  -rsync

import os
from subprocess import check_call


@target('null', 'null', std_dirs=False)
def build_null(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                'null/', path])


@target('zero', 'zero', std_dirs=False)
def build_zero(path):
    os.makedirs(os.path.join(path, 'var/tftpboot'))
    check_call(['rsync', '-rlp', '--exclude', '.*',
                'zero/', path])
