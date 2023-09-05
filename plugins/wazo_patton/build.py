"""
Copyright 2016-2023 The Wazo Authors  (see the AUTHORS file)
SPDX-License-Identifier: GPL-3.0-or-later

Depends on the following external programs:
 -rsync
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Callable
from subprocess import check_call

if TYPE_CHECKING:

    def target(
        target_id: str, plugin_id: str, std_dirs: bool = True
    ) -> Callable[[str], None]:
        """The `target` method is injected in `exec` call by the build script."""
        return lambda x: None


@target('6.11', 'wazo-patton-6.11')
def build_6_11(path: str) -> None:
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])
    check_call(['rsync', '-rlp', '--exclude', '.*', 'v6_11/', path])


@target('6.9', 'wazo-patton-6.9')
def build_6_9(path: str) -> None:
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])
    check_call(['rsync', '-rlp', '--exclude', '.*', 'v6_9/', path])
