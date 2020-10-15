# -*- coding: utf-8 -*-
# Copyright 2013-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

# Depends on the following external programs:
#  -rsync

from subprocess import check_call


@target('GXW4200', 'wazo-grandstream-GXW4200')
def build_GXW4200(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*',
                'GXW4200/', path])

