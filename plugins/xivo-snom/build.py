# -*- coding: utf-8 -*-

# Copyright (C) 2014-2016 Avencall
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


@target('8.7.5.35', 'xivo-snom-8.7.5.35')
def build_8_7_5_35(path):
    MODELS = [('300', 'f'),
              ('320', 'f'),
              ('370', 'f'),
              ('710', 'r'),
              ('715', 'r'),
              ('720', 'r'),
              ('725', 'r'),
              ('760', 'r'),
              ('D765', 'r'),
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
        sed_script = 's/#FW_FILENAME#/snom%s-8.7.5.35-SIP-%s.bin/' % (model, fw_suffix)
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
                '8.7.5.35/', path])


@target('8.9.3.40', 'xivo-snom-8.9.3.40')
def build_8_9_3_40(path):
    MODELS = [('D745', 'r')]

    check_call(['rsync', '-rlp', '--exclude', '.*',
                '--include', '/templates/base.tpl',
                '--include', '/templates/D745.tpl',
                '--exclude', '/templates/*.tpl',
                '--exclude', '*.btpl',
                'common/', path])

    for model, fw_suffix in MODELS:
        # generate snom<model>-firmware.xml.tpl from snom-model-firmware.xml.tpl.btpl
        model_tpl = os.path.join(path, 'templates', 'common', 'snom%s-firmware.xml.tpl' % model)
        sed_script = 's/#FW_FILENAME#/snom%s-8.9.3.40-SIP-%s.bin/' % (model, fw_suffix)
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
                '8.9.3.40/', path])

@target('8.9.3.60', 'xivo-snom-8.9.3.60')
def build_8_9_3_60(path):
    MODELS = [('D305', 'r'),
              ('D315', 'r'),
              ('D345', 'r'),
              ('D375', 'r'),
              ]

    check_call(['rsync', '-rlp', '--exclude', '.*',
                '--include', '/templates/base.tpl',
                '--include', '/templates/D3*5.tpl',
                '--exclude', '/templates/*.tpl',
                '--exclude', '*.btpl',
                'common/', path])

    for model, fw_suffix in MODELS:
        # generate snom<model>-firmware.xml.tpl from snom-model-firmware.xml.tpl.btpl
        model_tpl = os.path.join(path, 'templates', 'common', 'snom%s-firmware.xml.tpl' % model)
        sed_script = 's/#FW_FILENAME#/snom%s-8.9.3.60-SIP-%s.bin/' % (model, fw_suffix)
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
                '8.9.3.60/', path])

@target('8.9.3.80', 'xivo-snom-8.9.3.80')
def build_8_9_3_80(path):
    MODELS = [('D305', 'r'),
              ('D315', 'r'),
              ('D345', 'r'),
              ('D375', 'r'),
              ('710', 'r'),
              ('715', 'r'),
              ('720', 'r'),
              ('725', 'r'),
              ('760', 'r'),
              ('D765', 'r'),
              ('D745', 'r')
              ]

    check_call(['rsync', '-rlp', '--exclude', '.*',
                '--include', '/templates/base.tpl',
                '--include', '/templates/D3*5.tpl',
                '--exclude', '/templates/*.tpl',
                '--exclude', '*.btpl',
                'common/', path])

    for model, fw_suffix in MODELS:
        # generate snom<model>-firmware.xml.tpl from snom-model-firmware.xml.tpl.btpl
        model_tpl = os.path.join(path, 'templates', 'common', 'snom%s-firmware.xml.tpl' % model)
        sed_script = 's/#FW_FILENAME#/snom%s-8.9.3.80-SIP-%s.bin/' % (model, fw_suffix)
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
                '8.9.3.80/', path])
