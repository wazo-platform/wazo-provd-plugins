# -*- coding: utf-8 -*-

# Copyright 2018-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

# Depends on the following external programs:
#  -rsync

import os
from subprocess import check_call


@target('test-plugin', 'test-plugin')
def build_test_plugin(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                'test-plugin/', path])
