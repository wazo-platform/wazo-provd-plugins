# -*- coding: UTF-8 -*-

# Depends on the following external programs:
#  -rsync

from subprocess import check_call


@target('3.2.4B', 'xivo-polycom-3.2.4B')
def build_3_2_4B(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                '--include', '/templates/base.tpl',
                '--include', '/templates/SPIP320.tpl',
                '--include', '/templates/SPIP321.tpl',
                '--include', '/templates/SPIP330.tpl',
                '--include', '/templates/SPIP331.tpl',
                '--include', '/templates/SPIP335.tpl',
                '--include', '/templates/SPIP430.tpl',
                '--include', '/templates/SPIP450.tpl',
                '--include', '/templates/SPIP550.tpl',
                '--include', '/templates/SPIP560.tpl',
                '--include', '/templates/SPIP650.tpl',
                '--include', '/templates/SPIP670.tpl',
                '--include', '/templates/SSIP5000.tpl',
                '--include', '/templates/SSIP6000.tpl',
                '--include', '/templates/SSIP7000.tpl',
                '--exclude', '/templates/*',
                'common/', path])
    
    check_call(['rsync', '-rlp', '--exclude', '.*',
                '3.2.4B/', path])


@target('3.1.6', 'xivo-polycom-3.1.6')
def build_3_1_6(path):
    check_call(['rsync', '-rlp', '--exclude', '.*',
                '--include', '/templates/base.tpl',
                '--include', '/templates/SPIP301.tpl',
                '--include', '/templates/SPIP501.tpl',
                '--include', '/templates/SPIP600.tpl',
                '--include', '/templates/SPIP601.tpl',
                '--include', '/templates/SSIP4000.tpl',
                '--exclude', '/templates/*',
                'common/', path])
    
    check_call(['rsync', '-rlp', '--exclude', '.*',
                '3.1.6/', path])
