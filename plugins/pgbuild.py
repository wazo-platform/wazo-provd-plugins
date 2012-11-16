#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""A tool for building provd plugins."""

__license__ = """
    Copyright (C) 2010-2011  Avencall

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import errno
import glob
import hashlib
import json
import os
import shutil
import tarfile
import traceback
from itertools import izip_longest
from optparse import OptionParser
from subprocess import check_call
from sys import exit, stderr

BUILD_FILENAME = 'build.py'
DB_FILENAME = 'plugins.db'
PLUGIN_INFO_FILENAME = 'plugin-info'
PACKAGE_SUFFIX = '.tar.bz2'


def count(iterable, function=bool):
    """Return the number of element 'e' in iterable for which function(e) is
    true.
    
    If function is not specified, return the number of element 'e' in iterable
    which evaluates to true in a boolean context.
    
    """
    return len(filter(function, iterable))


def _is_bplugin(path):
    """Check if path is a bplugin.
    
    A path is a bplugin if it's a directory and has a file named BUILD_FILENAME
    inside it.
    
    """
    return os.path.isfile(os.path.join(path, BUILD_FILENAME))


def _list_bplugins(directory):
    def aux():
        for file in os.listdir(directory):
            file = os.path.join(directory, file)
            if _is_bplugin(file):
                yield file
    return list(aux())


def _mkdir(path):
    # Similar to os.mkdir but does not raise an exception if the directory
    # already exist
    try:
        os.mkdir(path)
    except OSError, e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


class Bplugin(object):
    def __init__(self, path):
        """Create a new Bplugin object.
        
        path -- the path to a bplugin [directory]
        
        """
        self._load_bplugin(path)
        self._bplugin_path = path
        self.name = os.path.basename(path)

    def _load_bplugin(self, path):
        targets = {}
        def _target(target_id, pg_id, std_dirs=True):
            def aux(fun):
                if target_id in targets:
                    raise Exception("in bplugin '%s': target redefinition for '%s'" %
                                    (self.name, target_id))
                targets[target_id] = {'fun': fun,
                                      'pg_id': pg_id,
                                      'std_dirs': std_dirs}
                return fun
            return aux
        build_file = os.path.join(path, BUILD_FILENAME)
        execfile(build_file, {'target': _target})
        self.targets = targets

    def build(self, target_id, pgdir):
        """Build the target plugin in pgdir.
        
        Note: pgdir is the base directory where plugins are created. The
        plugin will be created in a sub-directory.
        
        Raise a KeyError if target_id is not a valid target id.
        
        """
        target = self.targets[target_id]
        path = os.path.join(pgdir, target['pg_id'])
        os.mkdir(path)
        # assert: path is empty
        old_cwd = os.getcwd()
        abs_path = os.path.abspath(path)
        os.chdir(self._bplugin_path)
        try:
            # assert: current directory is the one of the bplugin
            target['fun'](abs_path)
        finally:
            os.chdir(old_cwd)
        if target['std_dirs']:
            self._mk_std_dirs(abs_path)

    def _mk_std_dirs(self, abs_path):
        for dir in ['var', 'var/cache', 'var/installed', 'var/templates', 'var/tftpboot']:
            _mkdir(os.path.join(abs_path, dir))


def build_op(opts, args, src_dir, dest_dir):
    # Pre: src_dir is a directory
    # Pre: dest_dir is a directory
    bdir = src_dir
    pgdir = dest_dir

    # parse bplugins and target to build
    if args:
        bplugin_path = os.path.join(bdir, args[0])
        bplugins_target = {bplugin_path: args[1:]}
    else:
        # build all plugins from all bplugins
        bplugins_target = {}
        for bplugin_path in _list_bplugins(bdir):
            bplugins_target[bplugin_path] = None

    # create bplugins object and check targets
    bplugins_obj = {}
    for bplugin_path, targets in bplugins_target.iteritems():
        try:
            bplugin = Bplugin(bplugin_path)
        except Exception, e:
            print >> stderr, "error: while loading bplugin '%s': %s" % (bplugin_path, e)
            exit(1)
        else:
            bplugins_obj[bplugin_path] = bplugin
            if not targets:
                bplugins_target[bplugin_path] = bplugin.targets.keys()
            else:
                for target_id in targets:
                    if target_id not in bplugin.targets:
                        print >> stderr, "error: target '%s' not in bplugin '%s'" % \
                              (target_id, bplugin_path)
                        exit(1)

    # build bplugins
    for bplugin_path, targets in bplugins_target.iteritems():
        print "Processing targets for bplugin '%s'..." % bplugin_path
        bplugin = bplugins_obj[bplugin_path]
        for target_id in targets:
            path = os.path.join(pgdir, bplugin.targets[target_id]['pg_id'])
            if os.path.exists(path):
                shutil.rmtree(path, False)
            print "  - Building target '%s' in directory '%s'..." % \
                  (target_id, path)
            try:
                bplugin.build(target_id, pgdir)
            except Exception:
                print >> stderr, "error while building target '%s':" % target_id
                traceback.print_exc(None, stderr)


def _is_plugin(path):
    return os.path.isfile(os.path.join(path, PLUGIN_INFO_FILENAME))


def _list_plugins(directory):
    def aux():
        for file in os.listdir(directory):
            file = os.path.join(directory, file)
            if _is_plugin(file):
                yield file
    return list(aux())


def _get_plugin_version(plugin):
    # Pre: plugin is a directory with an PLUGIN_INFO_FILENAME file
    fobj = open(os.path.join(plugin, PLUGIN_INFO_FILENAME))
    try:
        raw_plugin_info = json.load(fobj)
        return raw_plugin_info[u'version']
    except (ValueError, KeyError):
        print >> stderr, "error: plugin '%s' has invalid plugin info file" % plugin
        exit(1)
    finally:
        fobj.close()


def package_op(opts, args, src_dir, dest_dir):
    pg_dir = src_dir
    pkg_dir = dest_dir

    # parse plugins to package
    if args:
        plugins = [file for arg in args for file in glob.iglob(os.path.join(pg_dir, arg))]
        # make sure plugins are plugins...
        for plugin in plugins:
            if not _is_plugin(plugin):
                print >> stderr, "error: plugin '%s' is missing info file" % plugin
                exit(1)
    else:
        plugins = _list_plugins(pg_dir)

    # build packages
    for plugin in plugins:
        plugin_version = _get_plugin_version(plugin)
        package = "%s-%s%s" % (os.path.join(pkg_dir, os.path.basename(plugin)),
                               plugin_version, PACKAGE_SUFFIX)
        print "Packaging plugin '%s' into '%s'..." % (plugin, package)
        check_call(['tar', 'caf', package,
                    '-C', os.path.dirname(plugin) or os.curdir,
                    os.path.basename(plugin)])


def _list_packages(directory):
    return glob.glob(os.path.join(directory, '*' + PACKAGE_SUFFIX))


def _get_package_filename(package):
    return os.path.basename(package)


def _get_package_name(package):
    tar_package = tarfile.open(package)
    try:
        shortest_name = min(tar_package.getnames())
        if tar_package.getmember(shortest_name).isdir():
            return shortest_name
        else:
            print >> stderr, "error: package '%s' should have only 1 directory at depth 0" % package
            exit(1)
    finally:
        tar_package.close()


def _get_package_plugin_info(package, package_name):
    # Return a dictionary representing the standardized content of the
    # plugin-info file
    tar_package = tarfile.open(package)
    try:
        plugin_info_name = os.path.join(package_name, PLUGIN_INFO_FILENAME)
        if plugin_info_name not in tar_package.getnames():
            print >> stderr, "error: package '%s' has no file '%s'" % (package, plugin_info_name)
            exit(1)

        fobj = tar_package.extractfile(plugin_info_name)
        try:
            raw_plugin_info = json.load(fobj)
            for key in [u'capabilities', u'description', u'version']:
                if key not in raw_plugin_info:
                    raise ValueError()
            return raw_plugin_info
        except ValueError:
            print >> stderr, "error: package '%s' has invalid plugin-info file" % package
            exit(1)
        finally:
            fobj.close()
    finally:
        tar_package.close()


def _get_package_dsize(package):
    return os.path.getsize(package)


def _get_package_sha1sum(package):
    hash = hashlib.sha1()
    with open(package, 'rb') as fobj:
        hash.update(fobj.read())
    return hash.hexdigest()


def _get_package_info(package):
    # Return a tuple <package name, package info>
    result = {}
    result['filename'] = _get_package_filename(package)
    name = _get_package_name(package)
    result.update(_get_package_plugin_info(package, name))
    result['dsize'] = _get_package_dsize(package)
    result['sha1sum'] = _get_package_sha1sum(package)
    return name, result


def _version_cmp(version1, version2):
    """Compare the version version1 to version version2 and return:
    - negative if version1<version2
    - zero if version1==version2
    - positive if version1>version2.
    
    """
    start1, _, last1 = version1.rpartition('-')
    start2, _, last2 = version2.rpartition('-')
    for i1, i2 in izip_longest(start1.split('.'), start2.split('.'), fillvalue='0'):
        res_cmp = cmp(i1, i2)
        if res_cmp != 0:
            return res_cmp
    if not last1 and last2 or not last1.startswith('dev') and last2.startswith('dev'):
        return 1
    elif last1 and not last2 or last1.startswith('dev') and not last2.startswith('dev'):
        return -1
    return cmp(last1, last2)


def create_db_op(opts, args, src_dir, dest_dir):
    pkg_dir = src_dir
    db_file = os.path.join(dest_dir, DB_FILENAME)

    # parse packages to use to build db file
    if args:
        packages = [os.path.join(pkg_dir, arg) for arg in args]
    else:
        packages = _list_packages(pkg_dir)

    # get package infos, and only for the most recent packages
    package_infos = {}
    for package in packages:
        package_name, package_info = _get_package_info(package)
        if package_name in package_infos:
            cur_version = package_info['version']
            last_version = package_infos[package_name]['version']
            print >> stderr, "warning: found package %s in version %s and %s" % \
                  (package_name, cur_version, last_version)
            if _version_cmp(cur_version, last_version) > 0:
                package_infos[package_name] = package_info
        else:
            print "  Adding package '%s'..." % package
            package_infos[package_name] = package_info

    # create db file
    fobj = open(db_file, 'w')
    try:
        print "Creating DB file '%s'..." % db_file
        if opts.pretty_db:
            json.dump(package_infos, fobj, indent=4, sort_keys=True)
        else:
            json.dump(package_infos, fobj, separators=(',', ':'), sort_keys=True)
    finally:
        fobj.close()


def _get_directory(opt_value):
    # Return current dir if opt_value is none, else check if opt_value is
    # a directory and return it if it is, else write a message and exit
    if not opt_value:
        return os.curdir
    else:
        if not os.path.isdir(opt_value):
            print >> stderr, "error: '%s' is not a directory" % opt_value
            exit(1)
        return opt_value


def _get_directories(opts):
    # Return a tuple (source_dir, destination_dir)
    return _get_directory(opts.source), _get_directory(opts.destination)


def main():
    parser = OptionParser()
    parser.add_option('-B', '--build', action='store_true', dest='build',
                      help='create plugins from bplugins')
    parser.add_option('-P', '--package', action='store_true', dest='package',
                      help='create packages from plugins')
    parser.add_option('-D', '--db', action='store_true', dest='create_db',
                      help='create DB file from packages')
    parser.add_option('-s', '--source', dest='source',
                      help='source directory')
    parser.add_option('-d', '--destination', dest='destination',
                      help='destination directory')
    parser.add_option('--pretty-db', action='store_true', dest='pretty_db',
                      help='pretty format the DB file')

    opts, args = parser.parse_args()
    nb_op = count(getattr(opts, name) for name in ('build', 'package', 'create_db'))
    if nb_op != 1:
        print >> stderr, "error: only one operation may be used at a time (%s given)" % nb_op
        exit(1)
    # assert: only one operation is specified

    src_dir, dest_dir = _get_directories(opts)
    if opts.build:
        build_op(opts, args, src_dir, dest_dir)
    elif opts.package:
        package_op(opts, args, src_dir, dest_dir)
    elif opts.create_db:
        create_db_op(opts, args, src_dir, dest_dir)
    else:
        raise AssertionError('unknown operation... this is a bug')

main()
