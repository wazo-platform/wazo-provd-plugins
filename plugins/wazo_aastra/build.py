# Copyright 2014-2024 The Wazo Authors  (see the AUTHORS file)
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


@target('3.3.1-SP4', 'wazo-aastra-3.3.1-SP4')
def build_3_3_1_sp4(path: str) -> None:
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--exclude',
            '/templates/68*.tpl',
            'common/',
            path,
        ]
    )
    check_call(['rsync', '-rlp', '--exclude', '.*', 'v3_3_1_SP4/', path])


@target('4.3.0', 'wazo-aastra-4.3.0')
def build_4_3_0(path: str) -> None:
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--exclude',
            '/templates/67*',
            '--exclude',
            '/templates/9*',
            'common/',
            path,
        ]
    )
    check_call(['rsync', '-rlp', '--exclude', '.*', 'v4_3_0/', path])


@target('4.2.0', 'wazo-aastra-4.2.0')
def build_4_2_0(path: str) -> None:
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--exclude',
            '/templates/67*',
            '--exclude',
            '/templates/9*',
            'common/',
            path,
        ]
    )
    check_call(['rsync', '-rlp', '--exclude', '.*', 'v4_2_0/', path])


@target('5.0.0', 'wazo-aastra-5.0.0')
def build_5_0_0(path: str) -> None:
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--exclude',
            '/templates/67*',
            '--exclude',
            '/templates/9*',
            'common/',
            path,
        ]
    )
    check_call(['rsync', '-rlp', '--exclude', '.*', 'v5_0_0/', path])


@target('5.1.0', 'wazo-aastra-5.1.0')
def build_5_1_0(path: str) -> None:
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--exclude',
            '/templates/67*',
            '--exclude',
            '/templates/9*',
            '--exclude',
            '/templates/68*',
            'common/',
            path,
        ]
    )
    check_call(['rsync', '-rlp', '--exclude', '.*', 'v5_1_0/', path])
