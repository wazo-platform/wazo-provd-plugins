"""
Copyright 2014-2022 The Wazo Authors  (see the AUTHORS file)
SPDX-License-Identifier: GPL-3.0+

Depends on the following external programs:
 -rsync
"""

from subprocess import check_call


@target('7.5.5', 'wazo-cisco-spa-7.5.5')
def build_7_5_5(path):
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*', '7.5.5/', path])


@target('legacy', 'wazo-cisco-spa-legacy')
def build_legacy(path):
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*', 'legacy/', path])


@target('pap2t-5.1.6', 'wazo-cisco-pap2t-5.1.6')
def build_pap2t_5_1_6(path):
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*', 'pap2t-5.1.6/', path])


@target('spa100-1.3.5p', 'wazo-cisco-spa100-1.3.5p')
def build_spa100_1_3_5p(path):
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*', 'spa100-1.3.5p/', path])


@target('spa2102-5.2.12', 'wazo-cisco-spa2102-5.2.12')
def build_spa2102_5_2_12(path):
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*', 'spa2102-5.2.12/', path])


@target('spa3102-5.1.10', 'wazo-cisco-spa3102-5.1.10')
def build_spa3102_5_1_10(path):
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*', 'spa3102-5.1.10/', path])


@target('spa8000-6.1.11', 'wazo-cisco-spa8000-6.1.11')
def build_spa8000_6_1_11(path):
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*', 'spa8000-6.1.11/', path])


@target('spa8800-6.1.7', 'wazo-cisco-spa8800-6.1.7')
def build_spa8800_6_1_7(path):
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*', 'spa8800-6.1.7/', path])


@target('ata190-1.2.2', 'wazo-cisco-ata190-1.2.2')
def build_ata190_1_2_2(path):
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*', 'ata190-1.2.2/', path])
