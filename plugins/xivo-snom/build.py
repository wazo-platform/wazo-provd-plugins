# -*- coding: UTF-8 -*-

# Depends on the following external programs:
#  - rsync
#  - sed

import os.path
from shutil import copy
from subprocess import check_call


@target('8.7.3.15', 'xivo-snom-8.7.3.15')
def build_8_7_3_15(path):
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
        sed_script = 's/#FW_FILENAME#/snom%s-8.7.3.15-SIP-%s.bin/' % (model, fw_suffix)
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
                '8.7.3.15/', path])

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
