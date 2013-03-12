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

"""Plugin for Cisco phones using the 9.2.1/SCCP software."""

sccpcommon = {}
execfile_('sccpcommon.py', sccpcommon)


MODELS = [u'6901', u'6911', u'6921', u'6941', u'6945', u'6961', u'7906G',
          u'7911G', u'7931G', u'7941G', u'7942G', u'7945G', u'7961G',
          u'7962G', u'7965G', u'7970G', u'7971G', u'7975G']
VERSION = u'9.2.1/SCCP'
MODEL_VERSION = dict((m, VERSION) for m in MODELS)


class CiscoSccpPlugin(sccpcommon['BaseCiscoSccpPlugin']):
    IS_PLUGIN = True
    
    pg_associator = sccpcommon['common']['BaseCiscoPgAssociator'](MODEL_VERSION)
