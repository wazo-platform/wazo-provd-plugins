# Copyright 2010-2022 The Wazo Authors  (see the AUTHORS file)
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

import logging
import re
import os.path
from operator import itemgetter
from xml.sax.saxutils import escape
from provd import plugins
from provd import tzinform
from provd import synchronize
from provd.devices.config import RawConfigError
from provd.devices.pgasso import IMPROBABLE_SUPPORT, PROBABLE_SUPPORT,\
    COMPLETE_SUPPORT, BasePgAssociator
from provd.plugins import StandardPlugin, FetchfwPluginHelper,\
    TemplatePluginHelper
from provd.servers.http import HTTPNoListingFileService
from provd.util import norm_mac, format_mac
from twisted.internet import defer, threads

logger = logging.getLogger('plugin.xivo-polycom')


class BasePolycomHTTPDeviceInfoExtractor(object):
    _UA_REGEX = re.compile(r'^FileTransport Polycom\w+-(\w*?)-UA/([\d.]+)')
    _PATH_REGEX = re.compile(r'/(?!000000000000)([\da-f]{12})(?:\.cfg|-user\.cfg|-boot\.log|-phone\.cfg|-license\.cfg|-directory\.xml|-app\.log)$')
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
                if 'version' in dev_info and not self._is_sip_application_request(path):
                    del dev_info['version']
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
        #   "FileTransport PolycomSoundPointIP-SPIP_450-UA/3.2.3.1734" (SPIP450 3.2.3.1734/4.2.2.0710)
        #   "FileTransport PolycomSoundPointIP-SPIP_550-UA/3.2.3.1734" (SPIP335 3.2.3.1734/4.2.2.0710)
        #   "FileTransport PolycomSoundStationIP-SSIP_6000-UA/4.0.4.2906 Type/Application"
        #   "FileTransport PolycomSoundStationIP-SSIP_6000-UA/5.0.3.1667 Type/Updater"
        #   "FileTransport PolycomVVX-VVX_400-UA/4.1.4.7430 Type/Application"
        #   "FileTransport PolycomVVX-VVX_101-UA/5.4.3.1014 Type/Application"
        m = self._UA_REGEX.match(ua)
        if m:
            dev_info['vendor'] = 'Polycom'
            raw_model, raw_version = m.groups()
            dev_info['model'] = raw_model.replace('_', '').decode('ascii')
            dev_info['version'] = raw_version.decode('ascii')

    def _extract_mac_from_path(self, path, dev_info):
        # Extract the MAC address from the requested path if possible
        m = self._PATH_REGEX.search(path)
        if m:
            raw_mac = m.group(1)
            dev_info['mac'] = norm_mac(raw_mac.decode('ascii'))

    def _is_sip_application_request(self, path):
        # Return true if path has been requested by the SIP application (and
        # not the BootROM). This use the fact that some files are only
        # request by the SIP application.
        return self._IS_SIPAPP_REGEX.search(path)


class BasePolycomPgAssociator(BasePgAssociator):

    def __init__(self, models):
        BasePgAssociator.__init__(self)
        self._models = models

    def _do_associate(self, vendor, model, version):
        if vendor == 'Polycom':
            if model in self._models:
                return COMPLETE_SUPPORT + 1
            return PROBABLE_SUPPORT
        return IMPROBABLE_SUPPORT


class BasePolycomPlugin(StandardPlugin):
    # Note that no TFTP support is included since Polycom phones are capable of
    # protocol selection via DHCP options.
    _ENCODING = 'UTF-8'
    _EXPANSION = 3 * 40  # Expansion modules
    _NB_FKEY = {
        'SPIP450': 2,
        'SPIP550': 3,
        'SPIP560': 3,
        'SPIP650': 47,
        'SPIP670': 47,
        'VVX101': 2,
        'VVX150': 2,
        'VVX200': 2,
        'VVX201': 2,
        'VVX250': 4,
        'VVX300': 6 + _EXPANSION,
        'VVX301': 6 + _EXPANSION,
        'VVX310': 6 + _EXPANSION,
        'VVX311': 6 + _EXPANSION,
        'VVX350': 6,
        'VVX400': 12 + _EXPANSION,
        'VVX401': 12 + _EXPANSION,
        'VVX410': 12 + _EXPANSION,
        'VVX411': 12 + _EXPANSION,
        'VVX450': 12 + _EXPANSION,
        'VVX500': 12 + _EXPANSION,
        'VVX501': 12 + _EXPANSION,
        'VVX600': 16 + _EXPANSION,
        'VVX601': 16 + _EXPANSION,
        'VVX1500': 6,
    }
    _LOCALE = {
        'de_DE': 'German_Germany',
        'en_US': 'English_United_States',
        'es_ES': 'Spanish_Spain',
        'fr_FR': 'French_France',
        'fr_CA': 'French_France',
        'it_IT': 'Italian_Italy',
        'nl_NL': 'Dutch_Netherlands',
    }
    _SYSLOG_LEVEL = {
        'critical': '5',
        'error': '4',
        'warning': '3',
        'info': '2',
        'debug': '1'
    }
    _SYSLOG_LEVEL_DEF = '1'
    _SIP_TRANSPORT = {
        'udp': 'UDPOnly',
        'tcp': 'TCPOnly',
        'tls': 'TLS'
    }
    _SIP_TRANSPORT_DEF = 'UDPOnly'
    _XX_DICT_DEF = 'en'
    _XX_DICT = {
        'en': {
            'remote_directory': 'Directory',
        },
        'fr': {
            'remote_directory': 'Annuaire',
        },
    }

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
        lines.append('tcpIpApp.sntp.daylightSavings.%s.month="%d"' % (suffix, dst_change['month']))
        lines.append('tcpIpApp.sntp.daylightSavings.%s.time="%d"' % (suffix, dst_change['time'].as_hours))
        if dst_change['day'].startswith('D'):
            lines.append('tcpIpApp.sntp.daylightSavings.%s.date="%s"' % (suffix, dst_change['day'][1:]))
        else:
            week, weekday = dst_change['day'][1:].split('.')
            lines.append('tcpIpApp.sntp.daylightSavings.%s.dayOfWeek="%s"' % (suffix, weekday))
            if week == '5':
                lines.append('tcpIpApp.sntp.daylightSavings.%s.dayOfWeek.lastInMonth="1"' % suffix)
            else:
                lines.append('tcpIpApp.sntp.daylightSavings.%s.dayOfWeek.lastInMonth="0"' % suffix)
                lines.append('tcpIpApp.sntp.daylightSavings.%s.date="%d"' % (suffix, (int(week) - 1) * 7 + 1))
        return lines

    def _format_tzinfo(self, tzinfo):
        lines = []
        lines.append('tcpIpApp.sntp.gmtOffset="%d"' % tzinfo['utcoffset'].as_seconds)
        if tzinfo['dst'] is None:
            lines.append('tcpIpApp.sntp.daylightSavings.enable="0"')
        else:
            lines.append('tcpIpApp.sntp.daylightSavings.enable="1"')
            if tzinfo['dst']['start']['day'].startswith('D'):
                lines.append('tcpIpApp.sntp.daylightSavings.fixedDayEnable="1"')
            else:
                lines.append('tcpIpApp.sntp.daylightSavings.fixedDayEnable="0"')
            lines.extend(self._format_dst_change('start', tzinfo['dst']['start']))
            lines.extend(self._format_dst_change('stop', tzinfo['dst']['end']))
        return '\n'.join(lines)

    def _add_timezone(self, raw_config):
        if 'timezone' in raw_config:
            try:
                tzinfo = tzinform.get_timezone_info(raw_config['timezone'])
            except tzinform.TimezoneNotFoundError as e:
                logger.info('Unknown timezone: %s', e)
            else:
                raw_config['XX_timezone'] = self._format_tzinfo(tzinfo)

    def _add_language(self, raw_config):
        locale = raw_config.get('locale')
        if locale in self._LOCALE:
            raw_config['XX_language'] = self._LOCALE[locale]

    def _add_fkeys(self, raw_config, model):
        if model not in self._NB_FKEY:
            logger.info('Unknown model or model with no funckeys: %s', model)
            return
        nb_keys = self._NB_FKEY[model]
        lines = []
        for funckey_no, funckey_dict in sorted(iter(raw_config['funckeys'].items()),
                                               key=itemgetter(0)):
            funckey_type = funckey_dict['type']
            if funckey_type == 'speeddial':
                logger.info('Polycom doesn\'t support non-supervised function keys')
            elif funckey_type != 'blf' and funckey_type != 'park':
                logger.info('Unsupported funckey type: %s', funckey_type)
                continue
            keynum = int(funckey_no)
            if keynum <= nb_keys:
                value = funckey_dict['value']
                lines.append('attendant.resourceList.%s.address="%s"' %
                             (funckey_no, value))
                lines.append('attendant.resourceList.%s.label="%s"' %
                             (funckey_no, escape(funckey_dict.get('label', value))))
            else:
                logger.info('Model %s has less than %s function keys', model, funckey_no)
        raw_config['XX_fkeys'] = '\n'.join(lines)

    def _add_syslog_level(self, raw_config):
        syslog_level = raw_config.get('syslog_level')
        raw_config['XX_syslog_level'] = self._SYSLOG_LEVEL.get(syslog_level,
                                                                self._SYSLOG_LEVEL_DEF)

    def _add_sip_transport(self, raw_config):
        raw_config['XX_sip_transport'] = self._SIP_TRANSPORT.get(raw_config.get('sip_transport'),
                                                                  self._SIP_TRANSPORT_DEF)

    def _add_xivo_phonebook_url(self, raw_config):
        if hasattr(plugins, 'add_xivo_phonebook_url') and raw_config.get('config_version', 0) >= 1:
            plugins.add_xivo_phonebook_url(raw_config, 'polycom')
        else:
            self._add_xivo_phonebook_url_compat(raw_config)

    def _add_xivo_phonebook_url_compat(self, raw_config):
        hostname = raw_config.get('X_xivo_phonebook_ip')
        if hostname:
            raw_config['XX_xivo_phonebook_url'] = 'http://{hostname}/service/ipbx/web_services.php/phonebook/search/'.format(hostname=hostname)

    def _update_sip_lines(self, raw_config):
        proxy_ip = raw_config.get('sip_proxy_ip')
        proxy_port = raw_config.get('sip_proxy_port', '')
        backup_proxy_ip = raw_config.get('sip_backup_proxy_ip', '')
        backup_proxy_port = raw_config.get('sip_backup_proxy_port', '')
        voicemail = raw_config.get('exten_voicemail')
        for line in raw_config['sip_lines'].values():
            line.setdefault('proxy_ip', proxy_ip)
            line.setdefault('proxy_port', proxy_port)
            line.setdefault('backup_proxy_ip', backup_proxy_ip)
            line.setdefault('backup_proxy_port', backup_proxy_port)
            if voicemail:
                line.setdefault('voicemail', voicemail)

    def _gen_xx_dict(self, raw_config):
        xx_dict = self._XX_DICT[self._XX_DICT_DEF]
        if 'locale' in raw_config:
            locale = raw_config['locale']
            lang = locale.split('_', 1)[0]
            if lang in self._XX_DICT:
                xx_dict = self._XX_DICT[lang]
        return xx_dict

    _SENSITIVE_FILENAME_REGEX = re.compile(r'^[0-9a-f]{12}-user\.cfg$')

    def _dev_specific_filename(self, device):
        # Return the device specific filename (not pathname) of device
        fmted_mac = format_mac(device['mac'], separator='')
        return '%s-user.cfg' % fmted_mac

    def _check_config(self, raw_config):
        if 'http_port' not in raw_config:
            raise RawConfigError('only support configuration via HTTP')

    def _check_device(self, device):
        if 'mac' not in device:
            raise Exception('MAC address needed for device configuration')

    def configure(self, device, raw_config):
        self._check_config(raw_config)
        self._check_device(device)
        filename = self._dev_specific_filename(device)
        tpl = self._tpl_helper.get_dev_template(filename, device)

        self._add_timezone(raw_config)
        self._add_language(raw_config)
        self._add_fkeys(raw_config, device.get('model'))
        self._add_syslog_level(raw_config)
        self._add_sip_transport(raw_config)
        self._add_xivo_phonebook_url(raw_config)
        self._update_sip_lines(raw_config)
        raw_config['XX_dict'] = self._gen_xx_dict(raw_config)
        raw_config['XX_options'] = device.get('options', {})

        path = os.path.join(self._tftpboot_dir, filename)
        self._tpl_helper.dump(tpl, raw_config, path, self._ENCODING)

    def deconfigure(self, device):
        path = os.path.join(self._tftpboot_dir, self._dev_specific_filename(device))
        try:
            os.remove(path)
        except OSError as e:
            logger.warning('error while deconfiguring device: %s', e)

    if hasattr(synchronize, 'standard_sip_synchronize'):
        def synchronize(self, device, raw_config):
            return synchronize.standard_sip_synchronize(device)

    else:
        # backward compatibility with older wazo-provd server
        def synchronize(self, device, raw_config):
            try:
                ip = device['ip'].encode('ascii')
            except KeyError:
                return defer.fail(Exception('IP address needed for device synchronization'))
            else:
                sync_service = synchronize.get_sync_service()
                if sync_service is None or sync_service.TYPE != 'AsteriskAMI':
                    return defer.fail(Exception('Incompatible sync service: %s' % sync_service))
                else:
                    return threads.deferToThread(sync_service.sip_notify, ip, 'check-sync')

    def get_remote_state_trigger_filename(self, device):
        if 'mac' not in device:
            return None

        return self._dev_specific_filename(device)

    def is_sensitive_filename(self, filename):
        return bool(self._SENSITIVE_FILENAME_REGEX.match(filename))
