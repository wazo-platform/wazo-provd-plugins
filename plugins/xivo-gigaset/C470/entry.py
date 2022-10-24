# Copyright (C) 2013-2022 The Wazo Authors  (see the AUTHORS file)
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

"""Plugin for various Gigaset using the 02227 firmware.

The following Gigaset phones are supported:
- C470 IP
- C475 IP (not tested)
- S675 IP
- S685 IP (not tested)

"""

import logging
import re

common_globals = {}
execfile_('common.py', common_globals)

logger = logging.getLogger('plugin.xivo-gigaset')


MODELS = ['C470 IP', 'C475 IP', 'S675 IP', 'S685 IP']


class GigasetRequestBroker(common_globals['BaseGigasetRequestBroker']):
    _VERSION_REGEX = re.compile(r'\b02(\d{3})')
    
    def disable_gigasetnet_line(self):
        # we need to first check if the line is enabled or not...
        with self.do_get_request('scripts/settings_telephony_voip_multi.js') as fobj:
            for line in fobj:
                if line.startswith('lines[6][4]='):
                    if line[12:13] == '1':
                        logger.debug('gigaset line is enabled')
                        break
                    else:
                        logger.debug('gigaset line is disabled')
                        return
            else:
                raise GigasetInteractionError('Could not determine gigaset line status')
        
        # assert: gigaset line is enabled
        raw_data = 'account_id=6'
        with self.do_post_request('settings_telephony_voip_multi.html', raw_data) as fobj:
            fobj.read()
    
    def set_mailboxes(self, dict_):
        # dict_ is a dictionary where keys are line number and values are
        # mailbox extensions number
        raw_data = {}
        for id_no in range(7):
            line_no = id_no + 1
            if line_no in dict_:
                raw_data[f'ad1_{id_no}'] = dict_[line_no]
                raw_data[f'ad2_{id_no}'] = 'on'
            else:
                raw_data[f'ad1_{id_no}'] = ''
        with self.do_post_request('settings_telephony_am.html', raw_data) as fobj:
            fobj.read()


class GigasetPlugin(common_globals['BaseGigasetPlugin']):
    IS_PLUGIN = True
    
    _BROKER_FACTORY = GigasetRequestBroker
    
    pg_associator = common_globals['BaseGigasetPgAssociator'](MODELS)
