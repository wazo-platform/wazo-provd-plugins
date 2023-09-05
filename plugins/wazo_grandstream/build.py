"""
Copyright 2013-2023 The Wazo Authors  (see the AUTHORS file)
SPDX-License-Identifier: GPL-3.0-or-later

Depends on the following external programs:
  -rsync
"""
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


@target('1.0.27.2', 'wazo-grandstream-1.0.27.2')
def build_1_0_27_2(path: str) -> None:
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/*',
            'common_ata/',
            path,
        ]
    )
    check_call(['rsync', '-rlp', '--exclude', '.*', 'v1_0_27_2/', path])


@target('1.0.3.27', 'wazo-grandstream-1.0.3.27')
def build_1_0_3_27(path: str) -> None:
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/*',
            'common/',
            path,
        ]
    )
    check_call(['rsync', '-rlp', '--exclude', '.*', 'v1_0_3_27/', path])


@target('1.0.3.2x-android', 'wazo-grandstream-1.0.3.2x-android')
def build_1_0_3_2x_android(path: str) -> None:
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/*',
            'common/',
            path,
        ]
    )
    check_call(['rsync', '-rlp', '--exclude', '.*', 'v1_0_3_2x_android/', path])


@target('1.0.5.48', 'wazo-grandstream-1.0.5.48')
def build_1_0_5_48(path: str) -> None:
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/*',
            'common/',
            path,
        ]
    )
    check_call(['rsync', '-rlp', '--exclude', '.*', 'v1_0_5_48/', path])


@target('1.0.7.13', 'wazo-grandstream-1.0.7.13')
def build_1_0_7_13(path: str) -> None:
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/*',
            'common/',
            path,
        ]
    )
    check_call(['rsync', '-rlp', '--exclude', '.*', 'v1_0_7_13/', path])


@target('1.0.8.6', 'wazo-grandstream-1.0.8.6')
def build_1_0_8_6(path: str) -> None:
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/*',
            'common/',
            path,
        ]
    )
    check_call(['rsync', '-rlp', '--exclude', '.*', 'v1_0_8_6/', path])


@target('1.0.8.9', 'wazo-grandstream-1.0.8.9')
def build_1_0_8_9(path: str) -> None:
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/*',
            'common/',
            path,
        ]
    )
    check_call(['rsync', '-rlp', '--exclude', '.*', 'v1_0_8_9/', path])


@target('1.2.5.3', 'wazo-grandstream-1.2.5.3')
def build_1_2_5_3(path: str) -> None:
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/*',
            'common/',
            path,
        ]
    )
    check_call(['rsync', '-rlp', '--exclude', '.*', 'v1_2_5_3/', path])


@target('1.0.11.79', 'wazo-grandstream-1.0.11.79')
def build_1_0_11_79(path: str) -> None:
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/*',
            'common/',
            path,
        ]
    )
    check_call(['rsync', '-rlp', '--exclude', '.*', 'v1_0_11_79/', path])
