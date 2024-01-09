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


@target('N510', 'wazo-gigaset-N510')
def build_N510(path: str) -> None:
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])
    check_call(['rsync', '-rlp', '--exclude', '.*', 'N510/', path])


@target('N720', 'wazo-gigaset-N720')
def build_N720(path: str) -> None:
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])
    check_call(['rsync', '-rlp', '--exclude', '.*', 'N720/', path])


@target('N870-83.v2.39.0', 'wazo-gigaset-N870-83.v2.39.0')
def build_N870_83_v2_39_0(path: str) -> None:
    check_call(['rsync', '-rlp', '--exclude', '.*', 'N870_83_v2_39_0/', path])


@target('N870-83.v2.48.0', 'wazo-gigaset-N870-83.v2.48.0')
def build_N870_83_v2_48_0(path: str) -> None:
    check_call(['rsync', '-rlp', '--exclude', '.*', 'N870_83_v2_48_0/', path])


@target('Nx70-83.v2.49.1', 'wazo-gigaset-Nx70-83.v2.49.1')
def build_Nx70_83_v2_49_1(path: str) -> None:
    check_call(['rsync', '-rlp', '--exclude', '.*', 'Nx70_83_v2_49_1/', path])


@target('C470', 'wazo-gigaset-C470')
def build_C470(path: str) -> None:
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common_c/', path])
    check_call(['rsync', '-rlp', '--exclude', '.*', 'C470/', path])


@target('C590', 'wazo-gigaset-C590')
def build_C590(path: str) -> None:
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common_c/', path])
    check_call(['rsync', '-rlp', '--exclude', '.*', 'C590/', path])
