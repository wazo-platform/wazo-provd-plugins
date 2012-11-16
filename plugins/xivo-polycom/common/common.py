# -*- coding: UTF-8 -*-

"""Common code shared by the the various xivo-polycom plugins.

Support the IP301, IP320, IP321, IP330, IP331, IP335, IP430, IP450, IP501,
IP550, IP560, IP600, IP601, IP650, IP670, IP4000, IP5000, IP6000, IP7000 and
VVX1500.

"""

__license__ = """
    Copyright (C) 2010-2011  Avencall

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# TODO add DHCP device info extractor ? (see admin guide p.374)

import logging
import re
import os.path
from operator import itemgetter
from xml.sax.saxutils import escape
from provd import tzinform
from provd import synchronize
from provd.devices.config import RawConfigError
from provd.devices.pgasso import IMPROBABLE_SUPPORT, PROBABLE_SUPPORT,\
    COMPLETE_SUPPORT, FULL_SUPPORT, BasePgAssociator
from provd.plugins import StandardPlugin, FetchfwPluginHelper,\
    TemplatePluginHelper
from provd.servers.http import HTTPNoListingFileService
from provd.util import norm_mac, format_mac
from twisted.internet import defer, threads

logger = logging.getLogger('plugin.xivo-polycom')


class BasePolycomHTTPDeviceInfoExtractor(object):
    _UA_REGEX = re.compile(r'^FileTransport Polycom\w+-(\w*?)-UA/([\d.]+)$')
    _PATH_REGEX = re.compile(r'/(?!000000000000)([\da-f]{12})(?:\.cfg|-boot\.log|-phone\.cfg|-license\.cfg|-directory\.xml|-app\.log)$')
    _IS_SIPAPP_REGEX = re.compile(r'/(?:(?:common\.cfg|phone1\.cfg|sip\.cfg)|(?:[\da-f]{12}-(?:phone\.cfg|license\.cfg|directory\.xml|app\.log)))$')

    def extract(self, request, request_type):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request):
        ua = request.getHeader('User-Agent')
        if ua:
            dev_info = {}
            self._extract_info_from_ua(ua, dev_info)
            if dev_info:
                path = request.path
                if u'version' in dev_info and not self._is_sip_application_request(path):
                    del dev_info[u'version']
                self._extract_mac_from_path(path, dev_info)
                return dev_info
        return None

    def _extract_info_from_ua(self, ua, dev_info):
        # Note: depending on the boot step, the version number will either
        # be the BootROM version (first few requests) or the SIP application
        # version (later on in the boot process).
        # HTTP User-Agent:
        #   "FileTransport PolycomSoundPointIP-SPIP_335-UA/3.2.1.0078" (SPIP335 3.2.1.0078/4.2.1.0275)
        #   "FileTransport PolycomSoundPointIP-SPIP_335-UA/4.2.1.0275" (SPIP335 3.2.1.0078/4.2.1.0275)
        #   "FileTransport PolycomSoundPointIP-SPIP_335-UA/3.2.3.1734" (SPIP335 3.2.3.1734/4.2.2.0710)
        #   "FileTransport PolycomSoundPointIP-SPIP_335-UA/4.2.2.0710" (SPIP335 3.2.3.1734/4.2.2.0710)
        #   "FileTransport PolycomSoundPointIP-SPIP_450-UA/3.2.3.1734" (SPIP450 3.2.3.1734/4.2.2.0710)
        #   "FileTransport PolycomSoundPointIP-SPIP_550-UA/3.2.3.1734" (SPIP335 3.2.3.1734/4.2.2.0710)
        m = self._UA_REGEX.match(ua)
        if m:
            dev_info[u'vendor'] = u'Polycom'
            raw_model, raw_version = m.groups()
            dev_info[u'model'] = raw_model.replace('_', '').decode('ascii')
            dev_info[u'version'] = raw_version.decode('ascii')

    def _extract_mac_from_path(self, path, dev_info):
        # Extract the MAC address from the requested path if possible
        m = self._PATH_REGEX.search(path)
        if m:
            raw_mac = m.group(1)
            dev_info[u'mac'] = norm_mac(raw_mac.decode('ascii'))

    def _is_sip_application_request(self, path):
        # Return true if path has been requested by the SIP application (and
        # not the BootROM). This use the fact that some files are only
        # request by the SIP application.
        return self._IS_SIPAPP_REGEX.search(path)


class BasePolycomPgAssociator(BasePgAssociator):
    def __init__(self, models, version):
        BasePgAssociator.__init__(self)
        self._models = models
        self._version = version

    def _do_associate(self, vendor, model, version):
        if vendor == u'Polycom':
            if model in self._models:
                if version == self._version:
                    return FULL_SUPPORT
                return COMPLETE_SUPPORT
            return PROBABLE_SUPPORT
        return IMPROBABLE_SUPPORT


class BasePolycomPlugin(StandardPlugin):
    # Note that no TFTP support is included since Polycom phones are capable of
    # protocol selection via DHCP options.
    _ENCODING = 'UTF-8'
    _NB_FKEY = {
        u'SPIP450': 2,
        u'SPIP550': 3,
        u'SPIP560': 3,
        u'SPIP650': 47,
        u'SPIP670': 47,
    }
    _LOCALE = {
        u'de_DE': u'German_Germany',
        u'en_US': u'English_United_States',
        u'es_ES': u'Spanish_Spain',
        u'fr_FR': u'French_France',
        u'fr_CA': u'French_France',
        u'it_IT': u'Italian_Italy',
        u'nl_NL': u'Dutch_Netherlands',
    }
    _SYSLOG_LEVEL = {
        u'critical': u'5',
        u'error': u'4',
        u'warning': u'3',
        u'info': u'2',
        u'debug': u'1'
    }
    _SYSLOG_LEVEL_DEF = u'1'
    _SIP_TRANSPORT = {
        u'udp': u'UDPOnly',
        u'tcp': u'TCPOnly',
        u'tls': u'TLS'
    }
    _SIP_TRANSPORT_DEF = u'UDPOnly'

    def __init__(self, app, plugin_dir, gen_cfg, spec_cfg):
        StandardPlugin.__init__(self, app, plugin_dir, gen_cfg, spec_cfg)

        self._tpl_helper = TemplatePluginHelper(plugin_dir)

        downloaders = FetchfwPluginHelper.new_downloaders(gen_cfg.get('proxies'))
        fetchfw_helper = FetchfwPluginHelper(plugin_dir, downloaders)

        self.services = fetchfw_helper.services()
        self.http_service = HTTPNoListingFileService(self._tftpboot_dir)

    http_dev_info_extractor = BasePolycomHTTPDeviceInfoExtractor()

    def _format_dst_change(self, suffix, dst_change):
        lines = []
        lines.append(u'tcpIpApp.sntp.daylightSavings.%s.month="%d"' % (suffix, dst_change['month']))
        lines.append(u'tcpIpApp.sntp.daylightSavings.%s.time="%d"' % (suffix, dst_change['time'].as_hours))
        if dst_change['day'].startswith('D'):
            lines.append(u'tcpIpApp.sntp.daylightSavings.%s.date="%s"' % (suffix, dst_change['day'][1:]))
        else:
            week, weekday = dst_change['day'][1:].split('.')
            lines.append(u'tcpIpApp.sntp.daylightSavings.%s.dayOfWeek="%s"' % (suffix, weekday))
            if week == '5':
                lines.append(u'tcpIpApp.sntp.daylightSavings.%s.dayOfWeek.lastInMonth="1"' % suffix)
            else:
                lines.append(u'tcpIpApp.sntp.daylightSavings.%s.dayOfWeek.lastInMonth="0"' % suffix)
                lines.append(u'tcpIpApp.sntp.daylightSavings.%s.date="%d"' % (suffix, (int(week) - 1) * 7 + 1))
        return lines

    def _format_tzinfo(self, tzinfo):
        lines = []
        lines.append(u'tcpIpApp.sntp.gmtOffset="%d"' % tzinfo['utcoffset'].as_seconds)
        if tzinfo['dst'] is None:
            lines.append(u'tcpIpApp.sntp.daylightSavings.enable="0"')
        else:
            lines.append(u'tcpIpApp.sntp.daylightSavings.enable="1"')
            if tzinfo['dst']['start']['day'].startswith('D'):
                lines.append(u'tcpIpApp.sntp.daylightSavings.fixedDayEnable="1"')
            else:
                lines.append(u'tcpIpApp.sntp.daylightSavings.fixedDayEnable="0"')
            lines.extend(self._format_dst_change('start', tzinfo['dst']['start']))
            lines.extend(self._format_dst_change('stop', tzinfo['dst']['end']))
        return u'\n'.join(lines)

    def _add_timezone(self, raw_config):
        if u'timezone' in raw_config:
            try:
                tzinfo = tzinform.get_timezone_info(raw_config[u'timezone'])
            except tzinform.TimezoneNotFoundError, e:
                logger.info('Unknown timezone: %s', e)
            else:
                raw_config[u'XX_timezone'] = self._format_tzinfo(tzinfo)

    def _add_language(self, raw_config):
        locale = raw_config.get(u'locale')
        if locale in self._LOCALE:
            raw_config[u'XX_language'] = self._LOCALE[locale]

    def _add_fkeys(self, raw_config, model):
        if model not in self._NB_FKEY:
            logger.info(u'Unknown model or model with no funckeys: %s', model)
            return
        nb_keys = self._NB_FKEY[model]
        lines = []
        for funckey_no, funckey_dict in sorted(raw_config[u'funckeys'].iteritems(),
                                               key=itemgetter(0)):
            funckey_type = funckey_dict[u'type']
            if funckey_type == u'speeddial':
                logger.info('Polycom doesn\'t support non-supervised function keys')
            elif funckey_type != u'blf':
                logger.info('Unsupported funckey type: %s', funckey_type)
                continue
            keynum = int(funckey_no)
            if keynum <= nb_keys:
                value = funckey_dict[u'value']
                lines.append(u'attendant.resourceList.%s.address="%s"' %
                             (funckey_no, value))
                lines.append(u'attendant.resourceList.%s.label="%s"' %
                             (funckey_no, escape(funckey_dict.get(u'label', value))))
            else:
                logger.info('Model %s has less than %s function keys', model, funckey_no)
        raw_config[u'XX_fkeys'] = u'\n'.join(lines)

    def _add_syslog_level(self, raw_config):
        syslog_level = raw_config.get(u'syslog_level')
        raw_config[u'XX_syslog_level'] = self._SYSLOG_LEVEL.get(syslog_level,
                                                                self._SYSLOG_LEVEL_DEF)

    def _add_sip_transport(self, raw_config):
        raw_config[u'XX_sip_transport'] = self._SIP_TRANSPORT.get(raw_config.get(u'sip_transport'),
                                                                  self._SIP_TRANSPORT_DEF)

    def _strip_pem_cert(self, pem_cert):
        # Remove the header/footer of a pem certificate and return only the
        # base64 encoded part of the certificate.
        return pem_cert.replace('\n', '')[len('-----BEGIN CERTIFICATE-----'):
                                          -len('-----END CERTIFICATE-----')]

    def _add_custom_cert(self, raw_config):
        if u'sip_servers_root_and_intermediate_certificates' in raw_config:
            # Note that there's must be 1 and only 1 certificate in pem_cert,
            # i.e. list of certificates isn't accepted, but is not checked...
            pem_cert = raw_config[u'sip_servers_root_and_intermediate_certificates']
            raw_config[u'XX_custom_cert'] = self._strip_pem_cert(pem_cert)

    def _update_sip_lines(self, raw_config):
        proxy_ip = raw_config.get(u'sip_proxy_ip')
        proxy_port = raw_config.get(u'sip_proxy_port', u'')
        backup_proxy_ip = raw_config.get(u'sip_backup_proxy_ip', u'')
        backup_proxy_port = raw_config.get(u'sip_backup_proxy_port', u'')
        voicemail = raw_config.get(u'exten_voicemail')
        for line in raw_config[u'sip_lines'].itervalues():
            line.setdefault(u'proxy_ip', proxy_ip)
            line.setdefault(u'proxy_port', proxy_port)
            line.setdefault(u'backup_proxy_ip', backup_proxy_ip)
            line.setdefault(u'backup_proxy_port', backup_proxy_port)
            if voicemail:
                line.setdefault(u'voicemail', voicemail)

    def _dev_specific_filename(self, device):
        # Return the device specific filename (not pathname) of device
        fmted_mac = format_mac(device[u'mac'], separator='')
        return '%s-user.cfg' % fmted_mac

    def _check_config(self, raw_config):
        if u'http_port' not in raw_config:
            raise RawConfigError('only support configuration via HTTP')

    def _check_device(self, device):
        if u'mac' not in device:
            raise Exception('MAC address needed for device configuration')

    def configure(self, device, raw_config):
        self._check_config(raw_config)
        self._check_device(device)
        filename = self._dev_specific_filename(device)
        tpl = self._tpl_helper.get_dev_template(filename, device)

        self._add_timezone(raw_config)
        self._add_language(raw_config)
        self._add_fkeys(raw_config, device.get(u'model'))
        self._add_syslog_level(raw_config)
        self._add_sip_transport(raw_config)
        self._add_custom_cert(raw_config)
        self._update_sip_lines(raw_config)

        path = os.path.join(self._tftpboot_dir, filename)
        self._tpl_helper.dump(tpl, raw_config, path, self._ENCODING)

    def deconfigure(self, device):
        path = os.path.join(self._tftpboot_dir, self._dev_specific_filename(device))
        try:
            os.remove(path)
        except OSError, e:
            logger.warning('error while deconfiguring device: %s', e)

    def synchronize(self, device, raw_config):
        try:
            ip = device[u'ip'].encode('ascii')
        except KeyError:
            return defer.fail(Exception('IP address needed for device synchronization'))
        else:
            sync_service = synchronize.get_sync_service()
            if sync_service is None or sync_service.TYPE != 'AsteriskAMI':
                return defer.fail(Exception('Incompatible sync service: %s' % sync_service))
            else:
                return threads.deferToThread(sync_service.sip_notify, ip, 'check-sync')
