# Copyright (C) 2012-2022 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

# Depends on the following external programs:
#  -rsync

import os
from subprocess import check_call


@target('null', 'null', std_dirs=False)
def build_null(path):
    check_call(['rsync', '-rlp', '--exclude', '.*', 'null/', path])


@target('zero', 'zero', std_dirs=False)
def build_zero(path):
    os.makedirs(os.path.join(path, 'var/tftpboot'))
    check_call(['rsync', '-rlp', '--exclude', '.*', 'zero/', path])
