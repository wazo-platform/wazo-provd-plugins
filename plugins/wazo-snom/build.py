# -*- coding: utf-8 -*-

# Copyright 2014-2021 The Wazo Authors (see AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

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
    MODELS = [
        ('D305', 'r'),
        ('D315', 'r'),
        ('D345', 'r'),
        ('D375', 'r'),
        ('710', 'r'),
        ('D712', 'r'),
        ('715', 'r'),
        ('720', 'r'),
        ('725', 'r'),
        ('D745', 'r'),
        ('760', 'r'),
        ('D765', 'r'),
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


@target('10.1.20.0', 'wazo-snom-10.1.20.0')
def build_10_1_20_0(path):
    MODELS = [
        ('D785', 'r'),
    ]
    check_call(['rsync', '-rlp', '--exclude', '.*',
                '--include', '/templates/base.tpl',
                '--include', '/templates/D785.tpl',
                '--exclude', '/templates/*.tpl',
                '--exclude', '*.btpl',
                'common/', path])

    for model, fw_suffix in MODELS:
        # generate snom<model>-firmware.xml.tpl from snom-model-firmware.xml.tpl.btpl
        model_tpl = os.path.join(path, 'templates', 'common', 'snom%s-firmware.xml.tpl' % model)
        sed_script = 's/#FW_FILENAME#/snom%s-10.1.20.0-SIP-%s.bin/' % (model, fw_suffix)
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
                '10.1.20.0/', path])


@target('10.1.26.1', 'wazo-snom-10.1.26.1')
def build_10_1_26_1(path):
    MODELS = [
        ('D735', 'r'),
    ]
    check_call(['rsync', '-rlp', '--exclude', '.*',
                '--include', '/templates/base.tpl',
                '--include', '/templates/D735.tpl',
                '--exclude', '/templates/*.tpl',
                '--exclude', '*.btpl',
                'common/', path])

    for model, fw_suffix in MODELS:
        # generate snom<model>-firmware.xml.tpl from snom-model-firmware.xml.tpl.btpl
        model_tpl = os.path.join(path, 'templates', 'common', 'snom%s-firmware.xml.tpl' % model)
        sed_script = 's/#FW_FILENAME#/snom%s-10.1.26.1-SIP-%s.bin/' % (model, fw_suffix)
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
                '10.1.26.1/', path])


@target('10.1.39.11', 'wazo-snom-10.1.39.11')
def build_10_1_39_11(path):
    MODELS = [
        ('D375', 'r'),
        ('715', 'r'),
        ('D717', 'r'),
        ('725', 'r'),
        ('D735', 'r'),
        ('D745', 'r'),
        ('D765', 'r'),
        ('D785', 'r'),
    ]
    check_call(['rsync', '-rlp', '--exclude', '.*',
                '--include', '/templates/base.tpl',
                '--include', '/templates/D7*5.tpl',
                '--include', '/templates/D375.tpl',
                '--include', '/templates/D717.tpl',
                '--exclude', '/templates/*.tpl',
                '--exclude', '*.btpl',
                'common/', path])

    for model, fw_suffix in MODELS:
        # generate snom<model>-firmware.xml.tpl from snom-model-firmware.xml.tpl.btpl
        model_tpl = os.path.join(path, 'templates', 'common', 'snom%s-firmware.xml.tpl' % model)
        sed_script = 's/#FW_FILENAME#/snom%s-10.1.39.11-SIP-%s.bin/' % (model, fw_suffix)
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
                '10.1.39.11/', path])


@target('10.1.46.16', 'wazo-snom-10.1.46.16')
def build_10_1_46_16(path):
    MODELS = [
        ('D120', 'r'),
        ('D305', 'r'),
        ('D315', 'r'),
        ('D335', 'r'),
        ('D345', 'r'),
        ('D375', 'r'),
        ('D385', 'r'),
        ('D712', 'r'),
        ('715', 'r'),
        ('D717', 'r'),
        ('725', 'r'),
        ('D735', 'r'),
        ('D745', 'r'),
        ('D765', 'r'),
        ('D785', 'r'),
    ]

    check_call(['rsync', '-rlp', '--exclude', '.*',
                '--include', '/templates/base.tpl',
                '--include', '/templates/D7*5.tpl',
                '--include', '/templates/D3*5.tpl',
                '--include', '/templates/D717.tpl',
                '--exclude', '/templates/*.tpl',
                '--exclude', '*.btpl',
                'common/', path])

    for model, fw_suffix in MODELS:
        # generate snom<model>-firmware.xml.tpl from snom-model-firmware.xml.tpl.btpl
        model_tpl = os.path.join(path, 'templates', 'common', 'snom%s-firmware.xml.tpl' % model)
        sed_script = 's/#FW_FILENAME#/snom%s-10.1.46.16-SIP-%s.bin/' % (model, fw_suffix)
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
                '10.1.46.16/', path])


@target('10.1.49.11', 'wazo-snom-10.1.49.11')
def build_10_1_49_11(path):
    MODELS = [
        ('D120', 'r'),
        ('D305', 'r'),
        ('D315', 'r'),
        ('D335', 'r'),
        ('D345', 'r'),
        ('D375', 'r'),
        ('D385', 'r'),
        ('D712', 'r'),
        ('715', 'r'),
        ('D717', 'r'),
        ('725', 'r'),
        ('D735', 'r'),
        ('D745', 'r'),
        ('D765', 'r'),
        ('D785', 'r'),
    ]

    check_call(['rsync', '-rlp', '--exclude', '.*',
                '--include', '/templates/base.tpl',
                '--include', '/templates/D7*5.tpl',
                '--include', '/templates/D3*5.tpl',
                '--include', '/templates/D717.tpl',
                '--exclude', '/templates/*.tpl',
                '--exclude', '*.btpl',
                'common/', path])

    for model, fw_suffix in MODELS:
        # generate snom<model>-firmware.xml.tpl from snom-model-firmware.xml.tpl.btpl
        model_tpl = os.path.join(path, 'templates', 'common', 'snom%s-firmware.xml.tpl' % model)
        sed_script = 's/#FW_FILENAME#/snom%s-10.1.46.16-SIP-%s.bin/' % (model, fw_suffix)
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
                '10.1.49.11/', path])


@target('10.1.51.12', 'wazo-snom-10.1.51.12')
def build_10_1_51_12(path):
    MODELS = [
        ('D120', 'r'),
        ('D305', 'r'),
        ('D315', 'r'),
        ('D335', 'r'),
        ('D345', 'r'),
        ('D375', 'r'),
        ('D385', 'r'),
        ('D712', 'r'),
        ('715', 'r'),
        ('D717', 'r'),
        ('725', 'r'),
        ('D735', 'r'),
        ('D745', 'r'),
        ('D765', 'r'),
        ('D785', 'r'),
    ]
    check_call(['rsync', '-rlp', '--exclude', '.*',
                '--include', '/templates/base.tpl',
                '--include', '/templates/D7*5.tpl',
                '--include', '/templates/D3*5.tpl',
                '--include', '/templates/D717.tpl',
                '--exclude', '/templates/*.tpl',
                '--exclude', '*.btpl',
                'common/', path])

    for model, fw_suffix in MODELS:
        # generate snom<model>-firmware.xml.tpl from snom-model-firmware.xml.tpl.btpl
        model_tpl = os.path.join(path, 'templates', 'common', 'snom%s-firmware.xml.tpl' % model)
        sed_script = 's/#FW_FILENAME#/snom%s-10.1.51.12-SIP-%s.bin/' % (model, fw_suffix)
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
                '10.1.51.12/', path])


@target('10.1.54.13', 'wazo-snom-10.1.54.13')
def build_10_1_54_13(path):
    MODELS = [
        ('D120', 'r'),
        ('D305', 'r'),
        ('D315', 'r'),
        ('D335', 'r'),
        ('D345', 'r'),
        ('D375', 'r'),
        ('D385', 'r'),
        ('D712', 'r'),
        ('715', 'r'),
        ('D717', 'r'),
        ('725', 'r'),
        ('D735', 'r'),
        ('D745', 'r'),
        ('D765', 'r'),
        ('D785', 'r'),
    ]
    check_call(['rsync', '-rlp', '--exclude', '.*',
                '--include', '/templates/base.tpl',
                '--include', '/templates/D7*5.tpl',
                '--include', '/templates/D3*5.tpl',
                '--include', '/templates/D717.tpl',
                '--exclude', '/templates/*.tpl',
                '--exclude', '*.btpl',
                'common/', path])

    for model, fw_suffix in MODELS:
        # generate snom<model>-firmware.xml.tpl from snom-model-firmware.xml.tpl.btpl
        model_tpl = os.path.join(path, 'templates', 'common', 'snom%s-firmware.xml.tpl' % model)
        sed_script = 's/#FW_FILENAME#/snom%s-10.1.54.13-SIP-%s.bin/' % (model, fw_suffix)
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
                '10.1.54.13/', path])


@target('05.20.0001', 'wazo-snom-dect-05.20.0001')
def build_05_20_0001(path):
    MODELS = [
        'M300',
        'M700',
        'M900',
    ]
    check_call(['rsync', '-rlp', '--exclude', '.*',
                '--include', '/templates/base.tpl',
                '--include', '/templates/M300.tpl',
                '--include', '/templates/M700.tpl',
                '--include', '/templates/M900.tpl',
                '--exclude', '/templates/*.tpl',
                '--exclude', '*.btpl',
                'common_dect/', path])

    for model in MODELS:
        # generate snom<model>-firmware.xml.tpl from snom-model-firmware.xml.tpl.btpl
        model_tpl = os.path.join(path, 'templates', 'common', 'snom%s-firmware.htm.tpl' % model)
        sed_script = 's/#FW_FILENAME#/%s_v0520_b0001.fwu/' % model
        with open(model_tpl, 'wb') as f:
            check_call(['sed', sed_script, 'common_dect/templates/common/snom-model-firmware.htm.tpl.btpl'],
                       stdout=f)

        # generate snom<model>.htm.tpl from snom-model.htm.tpl.mtpl
        model_tpl = os.path.join(path, 'templates', 'common', 'snom%s.htm.tpl' % model)
        sed_script = 's/#MODEL#/%s/' % model
        with open(model_tpl, 'wb') as f:
            check_call(['sed', sed_script, 'common_dect/templates/common/snom-model.htm.tpl.btpl'],
                       stdout=f)

        # generate snom<model>.xml.tpl from snom-model.xml.mtpl
        model_tpl = os.path.join(path, 'templates', 'common', 'snom%s.xml.tpl' % model)
        sed_script = 's/#MODEL#/%s/' % model
        with open(model_tpl, 'wb') as f:
            check_call(['sed', sed_script, 'common_dect/templates/common/snom-model.xml.tpl.btpl'],
                       stdout=f)

    check_call(['rsync', '-rlp', '--exclude', '.*',
                '05.20.0001/', path])
