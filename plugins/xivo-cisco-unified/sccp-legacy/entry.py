# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
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

"""Plugin for legacy Cisco phones using the SCCP software."""

sccpcommon = {}
execfile_('sccpcommon.py', sccpcommon)


MODEL_VERSION = {u'7902G': u'8.0.2/SCCP',
                 u'7905G': u'8.0.3/SCCP',
                 u'7910G': u'5.0.7/SCCP',
                 u'7912G': u'8.0.4/SCCP',
                 u'7940G': u'8.1.2/SCCP',
                 u'7960G': u'8.1.2/SCCP'}


class CiscoSccpPlugin(sccpcommon['BaseCiscoSccpPlugin']):
    IS_PLUGIN = True
    
    pg_associator = sccpcommon['common']['BaseCiscoPgAssociator'](MODEL_VERSION)
