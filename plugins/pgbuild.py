#!/usr/bin/env python3
"""
Copyright 2010-2023 The Wazo Authors  (see the AUTHORS file)
SPDX-License-Identifier: GPL-3.0-or-later

A tool for building provd plugins.
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import shutil
import tarfile
import traceback
from argparse import ArgumentParser
from itertools import zip_longest
from pathlib import Path
from subprocess import check_call
from sys import exit, stderr
from typing import Any, TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from typing import TypedDict, Literal
    from collections.abc import Iterable, Callable

    PhoneTypes = Literal[
        'ata',
        'conference',
        'deskphone',
        'dect',
        'doorphone',
        'gateway',
        'generic',
        'softphone',
    ]
    Protocols = Literal['sip', 'sccp']
    TargetCallback = Callable[[str], None]

    class TargetDict(TypedDict):
        fun: TargetCallback
        pg_id: str
        std_dirs: str

    class PluginCapabilities(TypedDict):
        lines: int
        high_availability: bool
        function_keys: int
        expansion_modules: int
        switchboard: int
        multicell: bool
        type: PhoneTypes
        protocol: Protocols

    class RawPluginInfo(TypedDict):
        version: str
        description: str
        capabilities: dict[str, PluginCapabilities]

    class PluginInfo(RawPluginInfo):
        filename: str
        dsize: int
        sha1sum: str


BUILD_FILENAME = 'build.py'
DB_FILENAME = 'plugins.db'
PLUGIN_INFO_FILENAME = 'plugin-info'
PACKAGE_SUFFIX = '.tar.bz2'


def cmp(a: Any, b: Any) -> bool:
    return (a > b) - (a < b)


def count(iterable: Iterable, function: Callable[[Any], bool] = bool):
    """Return the number of element 'e' in iterable for which function(e) is
    true.

    If function is not specified, return the number of element 'e' in iterable
    which evaluates to true in a boolean context.

    """
    return len(list(filter(function, iterable)))


def _is_build_plugin(path):
    """Check if path is a build_plugin.

    A path is a build_plugin if it's a directory and has a file named BUILD_FILENAME
    inside it.

    """
    return os.path.isfile(os.path.join(path, BUILD_FILENAME))


def _list_build_plugins(directory: str) -> list[str]:
    build_plugins: list[str] = []
    for file in os.listdir(directory):
        file = os.path.join(directory, file)
        if _is_build_plugin(file):
            build_plugins.append(file)
    return build_plugins


class BuildPlugin:
    def __init__(self, path):
        """Create a new BuildPlugin object.

        path -- the path to a build_plugin [directory]

        """
        self._load_build_plugin(path)
        self._build_plugin_path = path
        self.name = os.path.basename(path)

    def _load_build_plugin(self, path):
        targets: dict[str, TargetDict] = {}

        def _target(
            target_id: str, pg_id: str, std_dirs: bool = True
        ) -> Callable[[TargetCallback], TargetCallback]:
            def aux(fun: TargetCallback) -> TargetCallback:
                if target_id in targets:
                    raise Exception(
                        f"in build_plugin '{self.name}': target redefinition for '{target_id}'"
                    )
                targets[target_id] = {'fun': fun, 'pg_id': pg_id, 'std_dirs': std_dirs}
                return fun

            return aux

        build_file = os.path.join(path, BUILD_FILENAME)
        exec(
            compile(open(build_file, "rb").read(), build_file, 'exec'),
            {'target': _target},
        )
        self.targets = targets

    def build(self, target_id, pgdir):
        """Build the target plugin in pgdir.

        Note: pgdir is the base directory where plugins are created. The
        plugin will be created in a subdirectory.

        Raise a KeyError if target_id is not a valid target id.

        """
        target = self.targets[target_id]
        path = os.path.join(pgdir, target['pg_id'])
        os.mkdir(path)
        # assert: path is empty
        old_cwd = os.getcwd()
        abs_path = os.path.abspath(path)
        os.chdir(self._build_plugin_path)
        try:
            # assert: current directory is the one of the build_plugins
            target['fun'](abs_path)
        finally:
            os.chdir(old_cwd)
        if target['std_dirs']:
            self._mk_std_dirs(abs_path)

    @staticmethod
    def _mk_std_dirs(abs_path: str) -> None:
        for directory in [
            'var',
            'var/cache',
            'var/installed',
            'var/templates',
            'var/tftpboot',
        ]:
            os.makedirs(Path(abs_path) / directory, exist_ok=True)


def build_op(
    opts: argparse.Namespace, args: Sequence[str], src_dir: str, dest_dir: str
) -> None:
    # Pre: src_dir is a directory
    # Pre: dest_dir is a directory
    build_dir = src_dir
    package_dir = dest_dir

    # parse build_plugins and target to build
    if args:
        build_plugin_path = os.path.join(build_dir, args[0])
        build_plugin_targets = {build_plugin_path: args[1:]}
    else:
        # build all plugins from all build plugins
        build_plugin_targets = {}
        for build_plugin_path in _list_build_plugins(build_dir):
            build_plugin_targets[build_plugin_path] = None

    # create build plugin objects and check targets
    build_plugins = {}
    for build_plugin_path, targets in build_plugin_targets.items():
        try:
            build_plugin = BuildPlugin(build_plugin_path)
        except Exception as e:
            print(
                f"error: while loading build plugin '{build_plugin_path}': {e}",
                file=stderr,
            )
            exit(1)
        else:
            build_plugins[build_plugin_path] = build_plugin
            if not targets:
                build_plugin_targets[build_plugin_path] = list(build_plugin.targets)
                continue
            for target_id in targets:
                if target_id not in build_plugin.targets:
                    print(
                        f"error: target '{target_id}' not in build plugin '{build_plugin_path}'",
                        file=stderr,
                    )
                    exit(1)

    # build, build plugins
    for build_plugin_path, targets in build_plugin_targets.items():
        print(f"Processing targets for build plugin '{build_plugin_path}'...")
        build_plugin = build_plugins[build_plugin_path]
        for target_id in targets:
            path = os.path.join(package_dir, build_plugin.targets[target_id]['pg_id'])
            if os.path.exists(path):
                shutil.rmtree(path, False)
            print(f"  - Building target '{target_id}' in directory '{path}'...")
            try:
                build_plugin.build(target_id, package_dir)
            except Exception:
                print(f"error while building target '{target_id}':", file=stderr)
                traceback.print_exc(None, stderr)


def _is_plugin(path: str) -> bool:
    return (Path(path) / PLUGIN_INFO_FILENAME).is_file()


def _list_plugins(directory: str) -> list[str]:
    def aux():
        for file in os.listdir(directory):
            file = os.path.join(directory, file)
            if _is_plugin(file):
                yield file

    return list(aux())


def _get_plugin_version(plugin: str) -> str:
    # Pre: plugin is a directory with an PLUGIN_INFO_FILENAME file
    fobj = open(os.path.join(plugin, PLUGIN_INFO_FILENAME))
    try:
        raw_plugin_info = json.load(fobj)
        return raw_plugin_info['version']
    except (ValueError, KeyError):
        print(f"error: plugin '{plugin}' has invalid plugin info file", file=stderr)
        exit(1)
    finally:
        fobj.close()


def package_op(
    opts: argparse.Namespace, args: Sequence[str], src_dir: str, dest_dir: str
) -> None:
    pg_dir = src_dir
    pkg_dir = dest_dir

    # parse plugins to package
    if args:
        plugins = [
            file for arg in args for file in glob.iglob(os.path.join(pg_dir, arg))
        ]
        # make sure plugins are plugins...
        for plugin in plugins:
            if not _is_plugin(plugin):
                print(f"error: plugin '{plugin}' is missing info file", file=stderr)
                exit(1)
    else:
        plugins = _list_plugins(pg_dir)

    # build packages
    for plugin in plugins:
        plugin_version = _get_plugin_version(plugin)
        plugin_name = os.path.basename(plugin).replace('_', '-')
        package_path = os.path.join(pkg_dir, plugin_name)
        package = f"{package_path}-{plugin_version}{PACKAGE_SUFFIX}"
        print(f"Packaging plugin '{plugin}' into '{package}'...")
        check_call(
            [
                'tar',
                'caf',
                package,
                '-C',
                os.path.dirname(plugin) or os.curdir,
                os.path.basename(plugin),
            ]
        )


def _list_packages(directory: str) -> list[str]:
    return glob.glob(os.path.join(directory, '*' + PACKAGE_SUFFIX))


def _get_package_filename(package: str) -> str:
    return os.path.basename(package)


def _get_package_name(package: str) -> str:
    tar_package = tarfile.open(package)
    try:
        shortest_name = min(tar_package.getnames())
        if tar_package.getmember(shortest_name).isdir():
            return shortest_name
        print(
            f"error: package '{package}' should have only 1 directory at depth 0",
            file=stderr,
        )
        exit(1)
    finally:
        tar_package.close()


def _get_package_plugin_info(package: str, package_name: str) -> dict:
    # Return a dictionary representing the standardized content of the
    # plugin-info file
    tar_package = tarfile.open(package)
    try:
        plugin_info_name = os.path.join(package_name, PLUGIN_INFO_FILENAME)
        if plugin_info_name not in tar_package.getnames():
            print(
                f"error: package '{package}' has no file '{plugin_info_name}'",
                file=stderr,
            )
            exit(1)

        fobj = tar_package.extractfile(plugin_info_name)
        try:
            raw_plugin_info = json.load(fobj)
            for key in ['capabilities', 'description', 'version']:
                if key not in raw_plugin_info:
                    raise ValueError()
            return raw_plugin_info
        except ValueError:
            print(
                f"error: package '{package}' has invalid plugin-info file", file=stderr
            )
            exit(1)
        finally:
            fobj.close()
    finally:
        tar_package.close()


def _get_package_dsize(package: str) -> int:
    return os.path.getsize(package)


def _get_package_sha1sum(package: str) -> str:
    package_hash = hashlib.sha1()
    with open(package, 'rb') as f:
        package_hash.update(f.read())
    return package_hash.hexdigest()


def _get_package_info(package: str) -> tuple[str, PluginInfo]:
    result = {'filename': _get_package_filename(package)}
    name = _get_package_name(package)
    result.update(_get_package_plugin_info(package, name))
    result['dsize'] = _get_package_dsize(package)
    result['sha1sum'] = _get_package_sha1sum(package)
    return name, result


def _version_cmp(version1: str, version2: str) -> int | bool:
    """Compare the version version1 to version version2 and return:
    - negative if version1<version2
    - zero if version1==version2
    - positive if version1>version2.
    - or bool.. Will be evaluated as 0 or 1, but should be made explicit.
    """
    start1, _, last1 = version1.rpartition('-')
    start2, _, last2 = version2.rpartition('-')
    for i1, i2 in zip_longest(start1.split('.'), start2.split('.'), fillvalue='0'):
        res_cmp = cmp(i1, i2)
        if res_cmp != 0:
            return int(res_cmp)
    if not last1 and last2 or not last1.startswith('dev') and last2.startswith('dev'):
        return 1
    elif last1 and not last2 or last1.startswith('dev') and not last2.startswith('dev'):
        return -1
    return cmp(last1, last2)


def create_db_op(
    opts: argparse.Namespace, args: Sequence[str], src_dir: str, dest_dir: str
) -> None:
    pkg_dir = src_dir
    db_file = os.path.join(dest_dir, DB_FILENAME)

    # parse packages to use to build db file
    if args:
        packages = [os.path.join(pkg_dir, arg) for arg in args]
    else:
        packages = _list_packages(pkg_dir)

    # get package info, and only for the most recent packages
    package_infos = {}
    for package in packages:
        package_name, package_info = _get_package_info(package)
        if package_name in package_infos:
            cur_version = package_info['version']
            last_version = package_infos[package_name]['version']
            print(
                f"warning: found package {package_name} "
                f"in version {cur_version} and {last_version}",
                file=stderr,
            )
            if _version_cmp(cur_version, last_version) > 0:
                package_infos[package_name] = package_info
        else:
            print(f"  Adding package '{package}'...")
            package_infos[package_name] = package_info

    # create db file
    print(f"Creating DB file '{db_file}'...")
    dump_kwargs = {'indent': 4} if opts.pretty_db else {'separators': (',', ':')}
    with open(db_file, 'w') as f:
        json.dump(package_infos, fp=f, sort_keys=True, **dump_kwargs)


def _get_directory(opt_value):
    # Return current dir if opt_value is none, else check if opt_value is
    # a directory and return it if it is, else write a message and exit
    if not opt_value:
        return os.curdir
    if not os.path.isdir(opt_value):
        print(f"error: '{opt_value}' is not a directory", file=stderr)
        exit(1)
    return opt_value


def _get_directories(opts):
    # Return a tuple (source_dir, destination_dir)
    return _get_directory(opts.source), _get_directory(opts.destination)


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument(
        '-B',
        '--build',
        action='store_true',
        dest='build',
        help='create plugins from build_plugins',
    )
    parser.add_argument(
        '-P',
        '--package',
        action='store_true',
        dest='package',
        help='create packages from plugins',
    )
    parser.add_argument(
        '-D',
        '--db',
        action='store_true',
        dest='create_db',
        help='create DB file from packages',
    )
    parser.add_argument('-s', '--source', dest='source', help='source directory')
    parser.add_argument(
        '-d', '--destination', dest='destination', help='destination directory'
    )
    parser.add_argument(
        '--pretty-db',
        action='store_true',
        dest='pretty_db',
        help='pretty format the DB file',
    )

    options, args = parser.parse_known_args()
    nb_op = count(getattr(options, name) for name in ('build', 'package', 'create_db'))
    if nb_op != 1:
        print(
            f"error: only one operation may be used at a time ({nb_op} given)",
            file=stderr,
        )
        exit(1)
    # assert: only one operation is specified

    src_dir, dest_dir = _get_directories(options)
    if options.build:
        build_op(options, args, src_dir, dest_dir)
    elif options.package:
        package_op(options, args, src_dir, dest_dir)
    elif options.create_db:
        create_db_op(options, args, src_dir, dest_dir)
    else:
        raise AssertionError('unknown operation... this is a bug')


if __name__ == '__main__':
    main()
