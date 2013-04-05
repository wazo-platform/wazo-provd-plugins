# -*- coding: UTF-8 -*-

# Depends on the following external programs:
#  -rsync

from subprocess import check_call


# target(<target_id>, <pg_id>)
# any error raised will be considered a build error
# Pre: pg_dir is initially empty
# Pre: current directory is the one of the bplugin
@target('2.6.0.2019', 'xivo-aastra-2.6.0.2019')
def build_2_6_0_2019(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                '--exclude', '/templates/6735i.tpl',
                '--exclude', '/templates/6737i.tpl',
                '--exclude', '/templates/6739i.tpl',
                'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*',
                '2.6.0.2019/', path])


@target('3.2.2-SP3', 'xivo-aastra-3.2.2-SP3')
def build_3_2_2_sp3(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                '--exclude', '/templates/6751i.tpl',
                'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*',
                '3.2.2-SP3/', path])


@target('switchboard', 'xivo-aastra-switchboard')
def build_switchboard(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                '--include', '/templates/6731i.tpl',
                '--include', '/templates/6755i.tpl',
                '--include', '/templates/6757i.tpl',
                '--include', '/templates/base.tpl',
                '--exclude', '/templates/*',
                'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*',
                'switchboard/', path])
