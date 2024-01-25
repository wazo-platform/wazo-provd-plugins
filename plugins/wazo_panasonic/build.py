# Copyright 2013-2023 The Wazo Authors  (see the AUTHORS file)
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


@target('01.133', 'wazo-panasonic-01.133')
def build_01_133(path: str) -> None:
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
    check_call(['rsync', '-rlp', '--exclude', '.*', 'v01_133/', path])
