# Copyright 2013-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations
from typing import TYPE_CHECKING

import binascii
import os.path
import struct
import urllib.error
import urllib.parse
import urllib.request

from provd.util import format_mac

if TYPE_CHECKING:
    from typing import TypedDict
    from ..common.common import (  # noqa: F401
        BaseGrandstreamPlugin,
        BaseGrandstreamPgAssociator,
    )

    class CommonGlobalsDict(TypedDict):
        BaseGrandstreamPlugin: type[BaseGrandstreamPlugin]
        BaseGrandstreamPgAssociator: type[BaseGrandstreamPgAssociator]


common: CommonGlobalsDict = {}  # type: ignore[typeddict-item]
execfile_('common.py', common)  # type: ignore[name-defined]

MODELS = [
    'GXP2000',
]
VERSION = '1.2.5.3'


class GrandstreamPlugin(common['BaseGrandstreamPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True

    _MODELS = MODELS

    pg_associator = common['BaseGrandstreamPgAssociator'](MODELS, VERSION)

    def _dev_specific_filename(self, device: dict[str, str]) -> str:
        # Return the device specific filename (not pathname) of device
        formatted_mac = format_mac(device['mac'], separator='', uppercase=False)
        return f'cfg{formatted_mac}'

    def configure(self, device, raw_config):
        self._check_config(raw_config)
        self._check_device(device)
        self._check_lines_password(raw_config)
        self._add_timezone(raw_config)
        self._add_locale(raw_config)
        self._add_fkeys(raw_config)
        filename = self._dev_specific_filename(device)
        tpl = self._tpl_helper.get_dev_template('GXP2000', device)

        path = os.path.join(self._tftpboot_dir, filename)
        rawdata = self._tpl_helper.render(tpl, raw_config, self._ENCODING)

        # Prepare binary data
        config = ''
        for line in rawdata.splitlines():
            cleaned_line = line.strip()
            if cleaned_line:  # is not empty
                items = [x.strip() for x in cleaned_line.split('=')]
                if len(items) == 2:  # Only interested in pairs (name=value)
                    config += f'{items[0]}={urllib.parse.quote(items[1])}&'

        formatted_mac = format_mac(device['mac'], separator='', uppercase=False)
        config += f'gnkey={formatted_mac[2:6]}'
        b_config = config.encode('ascii')

        # Convert mac to binary
        b_mac = binascii.unhexlify(formatted_mac)

        # Make sure length is even bytewise
        if len(b_config) % 2 != 0:
            b_config += b'\x00'

        # Make sure length is even wordwise
        if len(b_config) % 4 != 0:
            b_config += b'\x00\x00'

        config_length = 8 + (len(b_config) / 2)

        b_length = struct.pack('>L', config_length)

        b_crlf = b'\x0D\x0A\x0D\x0A'
        b_string = b_length
        b_string += b_mac
        b_string += b_crlf
        b_string += b_config

        # check sum ...
        csv = 0
        for i in range(0, len(b_string), 2):
            chunk = b_string[i : i + 2]
            x = struct.unpack('>H', chunk)[0]
            csv += x
        csv = 0x10000 - csv
        csv &= 0xFFFF
        b_checksum = struct.pack('>H', csv)

        b_full_config = b_length + b_checksum + b_mac + b_crlf + b_config

        # Write config file
        with open(path, 'w') as content_file:
            content_file.write(b_full_config.decode('ascii'))

    def _format_line(self, code: str, value: str) -> str:
        return f'    {code} = {value}'
