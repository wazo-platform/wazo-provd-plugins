# -*- coding: utf-8 -*-

# Copyright 2013-2016 The Wazo Authors  (see the AUTHORS file)
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

import binascii
import os.path
import struct
import urllib
from provd.util import format_mac

common = {}
execfile_('common.py', common)

MODELS = [
    u'GXP2000',
]
VERSION = u'1.2.5.3'


class GrandstreamPlugin(common['BaseGrandstreamPlugin']):
    IS_PLUGIN = True

    _MODELS = MODELS

    pg_associator = common['BaseGrandstreamPgAssociator'](MODELS, VERSION)

    def _dev_specific_filename(self, device):
        # Return the device specific filename (not pathname) of device
        fmted_mac = format_mac(device[u'mac'], separator='', uppercase=False)
        return 'cfg' + fmted_mac

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

        # Convert to binary
        config = ''
        for line in rawdata.splitlines():
            cleanedLine = line.strip()
            if cleanedLine: # is not empty                    
                items = [x.strip() for x in cleanedLine.split('=')]
                if len(items) == 2: # Only interested in pairs (name=value)
                    config += items[0] + '=' + urllib.quote(items[1]) + '&'
            
        fmted_mac = format_mac(device[u'mac'], separator='', uppercase=False)
        short_mac = fmted_mac[2:6]
        config = config + 'gnkey=' + short_mac
        # Convert to ascii
        config = str(config)

        # Convert mac to binary
        b_mac = binascii.unhexlify(fmted_mac)
        
        # Make sure length is even bytewise
        if len(config) % 2 != 0:
            config += '\x00'

        # Make sure length is even wordwise
        if len(config) % 4 != 0:
            config += "\x00\x00"
            
        config_length = 8 + (len(config) / 2)
        
        b_length = struct.pack('>L', config_length)
                
        b_crlf = '\x0D\x0A\x0D\x0A'
        b_string = b_length
        b_string += b_mac
        b_string += b_crlf
        b_string += config
        
        # check sum ...
        csv = 0
        for i in range(0, len(b_string), 2):
            chunk = b_string[i:i+2]
            x = struct.unpack( '>H', chunk)[0];
            csv += x
        csv = 0x10000 - csv
        csv &= 0xFFFF
        b_checksum = struct.pack('>H', csv)
        
        b_config = b_length + b_checksum + b_mac + b_crlf + config
        
        # Write config file
        with open(path, 'w') as content_file:
            content_file.write(b_config)

    def _format_line(self, code, value):
        return u'    %s = %s' % (code, value)
