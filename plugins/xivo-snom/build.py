# -*- coding: utf-8 -*-

# Copyright (C) 2014 Avencall
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
#  - rsync
#  - sed

import os.path
from subprocess import check_call


@target('8.7.5.17', 'xivo-snom-8.7.5.17')
def build_8_7_5_17(path):
    MODELS = [('710', 'r'),
              ('715', 'r'),
              ('720', 'r'),
              ('760', 'r')]

    check_call(['rsync', '-rlp', '--exclude', '.*',
                '--exclude', '*.btpl',
                'common/', path])

    for model, fw_suffix in MODELS:
        # generate snom<model>-firmware.xml.tpl from snom-model-firmware.xml.tpl.btpl
        model_tpl = os.path.join(path, 'templates', 'common', 'snom%s-firmware.xml.tpl' % model)
        sed_script = 's/#FW_FILENAME#/snom%s-8.7.5.17-SIP-%s.bin/' % (model, fw_suffix)
        with open(model_tpl, 'wb') as f:
            check_call(['sed', sed_script, 'common/templates/common/snom-model-firmware.xml.tpl.btpl'],
                       stdout=f)

        # generate snom<model>.htm.tpl from snom-model.htm.tpl.mtpl
        model_tpl = os.path.join(path, 'templates', 'common', 'snom%s.htm.tpl' % model)
        sed_script = 's/#MODEL#/%s/' % model
        with open(model_tpl, 'wb') as f:
            check_call(['sed', sed_script, 'common/templates/common/snom-model.htm.tpl.btpl'],
                       stdout=f)

        # generate snom<model>.xml.tpl from snom-model.xml.mtpl
        model_tpl = os.path.join(path, 'templates', 'common', 'snom%s.xml.tpl' % model)
        sed_script = 's/#MODEL#/%s/' % model
        with open(model_tpl, 'wb') as f:
            check_call(['sed', sed_script, 'common/templates/common/snom-model.xml.tpl.btpl'],
                       stdout=f)

    check_call(['rsync', '-rlp', '--exclude', '.*',
                '8.7.5.17/', path])


@target('8.7.3.25.5', 'xivo-snom-8.7.3.25.5')
def build_8_7_3_25_5(path):
    MODELS = [('300', 'f'),
              ('320', 'f'),
              ('360', 'f'),
              ('370', 'f'),
              ('710', 'r'),
              ('720', 'r'),
              ('760', 'r'),
              ('820', 'r'),
              ('821', 'r'),
              ('870', 'r'),
              ('MP', 'r'),
              ('PA1', 'f')]

    check_call(['rsync', '-rlp', '--exclude', '.*',
                '--exclude', '*.btpl',
                'common/', path])

    for model, fw_suffix in MODELS:
        # generate snom<model>-firmware.xml.tpl from snom-model-firmware.xml.tpl.btpl
        model_tpl = os.path.join(path, 'templates', 'common', 'snom%s-firmware.xml.tpl' % model)
        sed_script = 's/#FW_FILENAME#/snom%s-8.7.3.25.5-SIP-%s.bin/' % (model, fw_suffix)
        with open(model_tpl, 'wb') as f:
            check_call(['sed', sed_script, 'common/templates/common/snom-model-firmware.xml.tpl.btpl'],
                       stdout=f)

        # generate snom<model>.htm.tpl from snom-model.htm.tpl.mtpl
        model_tpl = os.path.join(path, 'templates', 'common', 'snom%s.htm.tpl' % model)
        sed_script = 's/#MODEL#/%s/' % model
        with open(model_tpl, 'wb') as f:
            check_call(['sed', sed_script, 'common/templates/common/snom-model.htm.tpl.btpl'],
                       stdout=f)

        # generate snom<model>.xml.tpl from snom-model.xml.mtpl
        model_tpl = os.path.join(path, 'templates', 'common', 'snom%s.xml.tpl' % model)
        sed_script = 's/#MODEL#/%s/' % model
        with open(model_tpl, 'wb') as f:
            check_call(['sed', sed_script, 'common/templates/common/snom-model.xml.tpl.btpl'],
                       stdout=f)

    check_call(['rsync', '-rlp', '--exclude', '.*',
                '8.7.3.25.5/', path])


@target('8.7.4.8', 'xivo-snom-8.7.4.8')
def build_8_7_4_8(path):
    MODELS = [('300', 'f'),
              ('320', 'f'),
              ('370', 'f'),
              ('710', 'r'),
              ('720', 'r'),
              ('760', 'r'),
              ('820', 'r'),
              ('821', 'r'),
              ('870', 'r'),
              ('MP', 'r'),
              ('PA1', 'f')]

    check_call(['rsync', '-rlp', '--exclude', '.*',
                '--exclude', '*.btpl',
                'common/', path])

    for model, fw_suffix in MODELS:
        # generate snom<model>-firmware.xml.tpl from snom-model-firmware.xml.tpl.btpl
        model_tpl = os.path.join(path, 'templates', 'common', 'snom%s-firmware.xml.tpl' % model)
        sed_script = 's/#FW_FILENAME#/snom%s-8.7.4.8-SIP-%s.bin/' % (model, fw_suffix)
        with open(model_tpl, 'wb') as f:
            check_call(['sed', sed_script, 'common/templates/common/snom-model-firmware.xml.tpl.btpl'],
                       stdout=f)

        # generate snom<model>.htm.tpl from snom-model.htm.tpl.mtpl
        model_tpl = os.path.join(path, 'templates', 'common', 'snom%s.htm.tpl' % model)
        sed_script = 's/#MODEL#/%s/' % model
        with open(model_tpl, 'wb') as f:
            check_call(['sed', sed_script, 'common/templates/common/snom-model.htm.tpl.btpl'],
                       stdout=f)

        # generate snom<model>.xml.tpl from snom-model.xml.mtpl
        model_tpl = os.path.join(path, 'templates', 'common', 'snom%s.xml.tpl' % model)
        sed_script = 's/#MODEL#/%s/' % model
        with open(model_tpl, 'wb') as f:
            check_call(['sed', sed_script, 'common/templates/common/snom-model.xml.tpl.btpl'],
                       stdout=f)

    check_call(['rsync', '-rlp', '--exclude', '.*',
                '8.7.4.8/', path])
