# Copyright 2014-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

# Depends on the following external programs:
#  -rsync
from __future__ import annotations

from subprocess import check_call
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:

    def target(
        target_id: str, plugin_id: str, std_dirs: bool = True
    ) -> Callable[[Callable[[str], None]], None]:
        """The `target` method is injected in `exec` call by the build script."""

        def wrapper(func: Callable[[str], None]) -> None:
            pass

        return wrapper


@target('4.0.11', 'wazo-polycom-4.0.11')
def build_4_0_11(path: str) -> None:
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/base.tpl',
            '--include',
            '/templates/SPIP321.tpl',
            '--include',
            '/templates/SPIP331.tpl',
            '--include',
            '/templates/SPIP335.tpl',
            '--include',
            '/templates/SPIP450.tpl',
            '--include',
            '/templates/SPIP550.tpl',
            '--include',
            '/templates/SPIP560.tpl',
            '--include',
            '/templates/SPIP650.tpl',
            '--include',
            '/templates/SPIP670.tpl',
            '--include',
            '/templates/SSIP5000.tpl',
            '--include',
            '/templates/SSIP6000.tpl',
            '--include',
            '/templates/SSIP7000.tpl',
            '--exclude',
            '/templates/*',
            'common/',
            path,
        ]
    )
    check_call(['rsync', '-rlp', '--exclude', '.*', 'v4_0_11/', path])


@target('5.4.3', 'wazo-polycom-5.4.3')
def build_5_4_3(path: str) -> None:
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/base.tpl',
            '--include',
            '/templates/VVX101.tpl',
            '--include',
            '/templates/VVX201.tpl',
            '--include',
            '/templates/VVX300.tpl',
            '--include',
            '/templates/VVX310.tpl',
            '--include',
            '/templates/VVX400.tpl',
            '--include',
            '/templates/VVX410.tpl',
            '--include',
            '/templates/VVX500.tpl',
            '--include',
            '/templates/VVX600.tpl',
            '--include',
            '/templates/VVX1500.tpl',
            '--exclude',
            '/templates/*',
            'common/',
            path,
        ]
    )
    check_call(['rsync', '-rlp', '--exclude', '.*', 'v5_4_3/', path])


@target('5.5.1', 'wazo-polycom-5.5.1')
def build_5_5_1(path: str) -> None:
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/base.tpl',
            '--include',
            '/templates/VVX101.tpl',
            '--include',
            '/templates/VVX201.tpl',
            '--include',
            '/templates/VVX300.tpl',
            '--include',
            '/templates/VVX310.tpl',
            '--include',
            '/templates/VVX400.tpl',
            '--include',
            '/templates/VVX410.tpl',
            '--include',
            '/templates/VVX500.tpl',
            '--include',
            '/templates/VVX600.tpl',
            '--include',
            '/templates/VVX1500.tpl',
            '--exclude',
            '/templates/*',
            'common/',
            path,
        ]
    )
    check_call(['rsync', '-rlp', '--exclude', '.*', 'v5_5_1/', path])


@target('5.8.2', 'wazo-polycom-5.8.2')
def build_5_8_2(path: str) -> None:
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/base.tpl',
            '--include',
            '/templates/VVX101.tpl',
            '--include',
            '/templates/VVX150.tpl',
            '--include',
            '/templates/VVX201.tpl',
            '--include',
            '/templates/VVX250.tpl',
            '--include',
            '/templates/VVX300.tpl',
            '--include',
            '/templates/VVX301.tpl',
            '--include',
            '/templates/VVX310.tpl',
            '--include',
            '/templates/VVX311.tpl',
            '--include',
            '/templates/VVX350.tpl',
            '--include',
            '/templates/VVX400.tpl',
            '--include',
            '/templates/VVX401.tpl',
            '--include',
            '/templates/VVX410.tpl',
            '--include',
            '/templates/VVX411.tpl',
            '--include',
            '/templates/VVX450.tpl',
            '--include',
            '/templates/VVX500.tpl',
            '--include',
            '/templates/VVX501.tpl',
            '--include',
            '/templates/VVX600.tpl',
            '--include',
            '/templates/VVX601.tpl',
            '--include',
            '/templates/VVX1500.tpl',
            '--exclude',
            '/templates/*',
            'common/',
            path,
        ]
    )
    check_call(['rsync', '-rlp', '--exclude', '.*', 'v5_8_2/', path])


@target('5.9.2', 'wazo-polycom-5.9.2')
def build_5_9_2(path: str) -> None:
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/base.tpl',
            '--include',
            '/templates/VVX101.tpl',
            '--include',
            '/templates/VVX150.tpl',
            '--include',
            '/templates/VVX201.tpl',
            '--include',
            '/templates/VVX250.tpl',
            '--include',
            '/templates/VVX300.tpl',
            '--include',
            '/templates/VVX301.tpl',
            '--include',
            '/templates/VVX310.tpl',
            '--include',
            '/templates/VVX311.tpl',
            '--include',
            '/templates/VVX350.tpl',
            '--include',
            '/templates/VVX400.tpl',
            '--include',
            '/templates/VVX401.tpl',
            '--include',
            '/templates/VVX410.tpl',
            '--include',
            '/templates/VVX411.tpl',
            '--include',
            '/templates/VVX450.tpl',
            '--include',
            '/templates/VVX500.tpl',
            '--include',
            '/templates/VVX501.tpl',
            '--include',
            '/templates/VVX600.tpl',
            '--include',
            '/templates/VVX601.tpl',
            '--include',
            '/templates/VVX1500.tpl',
            '--exclude',
            '/templates/*',
            'common/',
            path,
        ]
    )
    check_call(['rsync', '-rlp', '--exclude', '.*', 'v5_9_2/', path])


@target('3.2.4B', 'wazo-polycom-3.2.4B')
def build_3_2_4B(path: str) -> None:
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/base.tpl',
            '--include',
            '/templates/SPIP320.tpl',
            '--include',
            '/templates/SPIP321.tpl',
            '--include',
            '/templates/SPIP330.tpl',
            '--include',
            '/templates/SPIP331.tpl',
            '--include',
            '/templates/SPIP335.tpl',
            '--include',
            '/templates/SPIP430.tpl',
            '--include',
            '/templates/SPIP450.tpl',
            '--include',
            '/templates/SPIP550.tpl',
            '--include',
            '/templates/SPIP560.tpl',
            '--include',
            '/templates/SPIP650.tpl',
            '--include',
            '/templates/SPIP670.tpl',
            '--include',
            '/templates/SSIP5000.tpl',
            '--include',
            '/templates/SSIP6000.tpl',
            '--include',
            '/templates/SSIP7000.tpl',
            '--exclude',
            '/templates/*',
            'common_v3/',
            path,
        ]
    )
    check_call(['rsync', '-rlp', '--exclude', '.*', 'v3_2_4B/', path])


@target('3.1.6', 'wazo-polycom-3.1.6')
def build_3_1_6(path: str) -> None:
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/base.tpl',
            '--include',
            '/templates/SPIP301.tpl',
            '--include',
            '/templates/SPIP501.tpl',
            '--include',
            '/templates/SPIP600.tpl',
            '--include',
            '/templates/SPIP601.tpl',
            '--include',
            '/templates/SSIP4000.tpl',
            '--exclude',
            '/templates/*',
            'common_v3/',
            path,
        ]
    )
    check_call(['rsync', '-rlp', '--exclude', '.*', 'v3_1_6/', path])
