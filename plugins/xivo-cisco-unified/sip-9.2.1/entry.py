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

"""Plugin for Cisco phones using the 9.2.1/SIP software."""

sipcommon = {}
execfile_('sipcommon.py', sipcommon)


MODELS = [u'8961', u'9951', u'9971']
VERSION = u'9.2.1/SIP'
MODEL_VERSION = dict((m, VERSION) for m in MODELS)


class CiscoSipPlugin(sipcommon['BaseCiscoSipPlugin']):
    IS_PLUGIN = True
    
    pg_associator = sipcommon['common']['BaseCiscoPgAssociator'](MODEL_VERSION)
