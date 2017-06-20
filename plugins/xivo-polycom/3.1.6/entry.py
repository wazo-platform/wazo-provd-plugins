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

"""Plugin for Polycom phones using the 3.1.6.0017 SIP application.

The following Polycom phones are supported:
- SPIP301
- SPIP501
- SPIP600
- SPIP601
- SSIP4000

"""

common_globals = {}
execfile_('common.py', common_globals)


MODELS = [u'SPIP301', u'SPIP501', u'SPIP600', u'SPIP601', u'SSIP4000']
VERSION = u'3.1.6.0017'


class PolycomPlugin(common_globals['BasePolycomPlugin']):
    IS_PLUGIN = True
    
    pg_associator = common_globals['BasePolycomPgAssociator'](MODELS, VERSION)
