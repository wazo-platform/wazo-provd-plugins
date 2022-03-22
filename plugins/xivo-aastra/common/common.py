# -*- coding: utf-8 -*-

# Copyright 2010-2020 The Wazo Authors  (see the AUTHORS file)
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

import errno
import logging
import re
import os.path
from operator import itemgetter
from provd import plugins
from provd import tzinform
from provd import synchronize
from provd.devices.config import RawConfigError
from provd.plugins import StandardPlugin, FetchfwPluginHelper, \
    TemplatePluginHelper
from provd.devices.pgasso import IMPROBABLE_SUPPORT, COMPLETE_SUPPORT, \
    FULL_SUPPORT, BasePgAssociator, UNKNOWN_SUPPORT
from provd.servers.http import HTTPNoListingFileService
from provd.util import norm_mac, format_mac
from twisted.internet import defer, threads

logger = logging.getLogger('plugin.xivo-aastra')


class BaseAastraHTTPDeviceInfoExtractor(object):
    _UA_REGEX = re.compile(r'^Aastra(\w+) MAC:([^ ]+) V:([^ ]+)-SIP$')
    _UA_MODELS_MAP = {
        '51i': u'6751i', # not tested
        '53i': u'6753i', # not tested
        '55i': u'6755i',
        '57i': u'6757i',
    }

    def extract(self, request, request_type):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request):
        ua = request.getHeader('User-Agent')
        if ua:
            return self._extract_from_ua(ua)
        return None

    def _extract_from_ua(self, ua):
        # HTTP User-Agent:
        #   "Aastra6731i MAC:00-08-5D-23-74-29 V:3.2.0.70-SIP"
        #   "Aastra6731i MAC:00-08-5D-23-73-01 V:3.2.0.1011-SIP"
        #   "Aastra6739i MAC:00-08-5D-13-CA-05 V:3.0.1.2024-SIP"
        #   "Aastra6739i MAC:00-08-5D-13-CA-05 V:3.2.1.1013-SIP"
        #   "Aastra6735i MAC:00-08-5D-2E-A0-94 V:3.2.2.6038-SIP"
        #   "Aastra6737i MAC:00-08-5D-30-A6-CE V:3.2.2.6038-SIP"
        #   "Aastra6863i MAC:00-08-5D-40-90-5F V:4.1.0.128-SIP"
        m = self._UA_REGEX.match(ua)
        if m:
            raw_model, raw_mac, raw_version = m.groups()
            try:
                mac = norm_mac(raw_mac.decode('ascii'))
            except ValueError, e:
                logger.warning('Could not normalize MAC address: %s', e)
            else:
                if raw_model in self._UA_MODELS_MAP:
                    model = self._UA_MODELS_MAP[raw_model]
                else:
                    model = raw_model.decode('ascii')
                return {u'vendor': u'Aastra',
                        u'model': model,
                        u'version': raw_version.decode('ascii'),
                        u'mac': mac}
        return None


class BaseAastraPgAssociator(BasePgAssociator):
    def __init__(self, model_versions):
        BasePgAssociator.__init__(self)
        self._model_versions = model_versions

    def _do_associate(self, vendor, model, version):
        if vendor == u'Aastra':
            if model in self._model_versions:
                if version == self._model_versions[model]:
                    return FULL_SUPPORT
                return COMPLETE_SUPPORT
            return UNKNOWN_SUPPORT
        return IMPROBABLE_SUPPORT


class AastraModel(object):

    def __init__(self, nb_prgkey=0, nb_topsoftkey=0, nb_softkey=0, nb_expmod=0, nb_expmodkey=0):
        self.nb_prgkey = nb_prgkey
        self.nb_topsoftkey = nb_topsoftkey
        self.nb_softkey = nb_softkey
        self.nb_expmod = nb_expmod
        self.nb_expmodkey = nb_expmodkey

    def get_keytype(self, funckey_no):
        for keytype, nb_key in self._keytypes():
            if funckey_no <= nb_key:
                return keytype + unicode(funckey_no)
            funckey_no -= nb_key
        return None

    def _keytypes(self):
        yield (u'prgkey', self.nb_prgkey)
        yield (u'topsoftkey', self.nb_topsoftkey)
        yield (u'softkey', self.nb_softkey)
        for expmod_num in xrange(1, self.nb_expmod + 1):
            yield (u'expmod%s key' % expmod_num, self.nb_expmodkey)


class BaseAastraPlugin(StandardPlugin):
    _ENCODING = 'UTF-8'
    _M670_NB_KEY = 36
    _M675_NB_KEY = 60
    _M680_NB_KEY = 16
    _M685_NB_KEY = 84
    _MODELS = {
        u'6730i': AastraModel(
            nb_prgkey=8,
        ),
        u'6731i': AastraModel(
            nb_prgkey=8,
        ),
        u'6735i': AastraModel(
            nb_prgkey=6,
            nb_softkey=20,
            nb_expmod=3,
            nb_expmodkey=max(_M670_NB_KEY, _M675_NB_KEY),
        ),
        u'6737i': AastraModel(
            nb_topsoftkey=10,
            nb_softkey=20,
            nb_expmod=3,
            nb_expmodkey=max(_M670_NB_KEY, _M675_NB_KEY),
        ),
        u'6739i': AastraModel(
            nb_softkey=55,
            nb_expmod=3,
            nb_expmodkey=max(_M670_NB_KEY, _M675_NB_KEY),
        ),
        u'6753i': AastraModel(
            nb_prgkey=6,
            nb_expmod=3,
            nb_expmodkey=max(_M670_NB_KEY, _M675_NB_KEY),
        ),
        u'6755i': AastraModel(
            nb_prgkey=6,
            nb_softkey=20,
            nb_expmod=3,
            nb_expmodkey=max(_M670_NB_KEY, _M675_NB_KEY),
        ),
        u'6757i': AastraModel(
            nb_topsoftkey=10,
            nb_softkey=20,
            nb_expmod=3,
            nb_expmodkey=max(_M670_NB_KEY, _M675_NB_KEY),
        ),
        u'6863i': AastraModel(
            nb_prgkey=3,
        ),
        u'6865i': AastraModel(
            nb_prgkey=8,
            nb_expmod=3,
            nb_expmodkey=max(_M680_NB_KEY, _M685_NB_KEY),
        ),
        u'6867i': AastraModel(
            nb_topsoftkey=20,
            nb_softkey=18,
            nb_expmod=3,
            nb_expmodkey=max(_M680_NB_KEY, _M685_NB_KEY),
        ),
        u'6869i': AastraModel(
            nb_topsoftkey=44,
            nb_softkey=24,
            nb_expmod=3,
            nb_expmodkey=max(_M680_NB_KEY, _M685_NB_KEY),
        ),
        u'6873i': AastraModel(
            nb_topsoftkey=48,
            nb_softkey=24,
            nb_expmod=3,
            nb_expmodkey=max(_M680_NB_KEY, _M685_NB_KEY),
        ),
        u'6930': AastraModel(
            nb_topsoftkey=44,
            nb_softkey=24,
            nb_expmod=3,
            nb_expmodkey=max(_M680_NB_KEY, _M685_NB_KEY),
        ),
        u'9143i': AastraModel(
            nb_prgkey=7,
        ),
        u'9480i': AastraModel(
            nb_softkey=6,
        ),
    }
    _TRUSTED_ROOT_CERTS_SUFFIX = '-ca_servers.crt'
    _LOCALE = {
        # <locale>: (<lang file>, <tone set>, <input language>)
        u'de_DE': (u'lang_de.txt', u'Germany', u'German'),
        u'es_ES': (u'lang_es.txt', u'Europe', u'Spanish'),
        u'fr_FR': (u'lang_fr.txt', u'France', u'French'),
        u'fr_CA': (u'lang_fr_ca.txt', u'US', u'French'),
        u'it_IT': (u'lang_it.txt', u'Italy', u'Italian'),
        u'nl_NL': (u'lang_nl_nl.txt', u'Germany', u'Dutch'),
    }
    _SIP_DTMF_MODE = {
        # <dtmf mode>: (<out-of-band dtmf>, <dtmf method>)
        u'RTP-in-band': (u'0', u'0'),
        u'RTP-out-of-band': (u'1', u'0'),
        u'SIP-INFO': (u'1', u'1')
    }
    _SIP_SRTP_MODE = {
        u'disabled': u'0',
        u'preferred': u'1',
        u'required': u'2'
    }
    _SIP_TRANSPORT = {
        u'udp': u'1',
        u'tcp': u'2',
        u'tls': u'4'
    }
    _SYSLOG_LEVEL = {
        u'critical': u'1',
        u'error': u'3',
        u'warning': u'7',
        u'info': u'39',
        u'debug': u'65535'
    }
    _XX_DICT_DEF = u'en'
    _XX_DICT = {
        u'en': {
            u'voicemail':  u'Voicemail',
            u'fwd_unconditional': u'Unconditional forward',
            u'dnd': u'D.N.D',
            u'local_directory': u'Directory',
            u'callers': u'Callers',
            u'services': u'Services',
            u'pickup_call': u'Call pickup',
            u'remote_directory': u'Directory',
        },
        u'fr': {
            u'voicemail':  u'Messagerie',
            u'fwd_unconditional': u'Renvoi inconditionnel',
            u'dnd': u'N.P.D',
            u'local_directory': u'Repertoire',
            u'callers': u'Appels',
            u'services': u'Services',
            u'pickup_call': u'Interception',
            u'remote_directory': u'Annuaire',
        },
    }

    def __init__(self, app, plugin_dir, gen_cfg, spec_cfg):
        StandardPlugin.__init__(self, app, plugin_dir, gen_cfg, spec_cfg)
        # update to use the non-standard tftpboot directory
        self._base_tftpboot_dir = self._tftpboot_dir
        self._tftpboot_dir = os.path.join(self._tftpboot_dir, 'Aastra')

        self._tpl_helper = TemplatePluginHelper(plugin_dir)

        downloaders = FetchfwPluginHelper.new_downloaders(gen_cfg.get('proxies'))
        fetchfw_helper = FetchfwPluginHelper(plugin_dir, downloaders)
        # update to use the non-standard tftpboot directory
        fetchfw_helper.root_dir = self._tftpboot_dir

        self.services = fetchfw_helper.services()
        self.http_service = HTTPNoListingFileService(self._base_tftpboot_dir)

    http_dev_info_extractor = BaseAastraHTTPDeviceInfoExtractor()

    def _add_out_of_band_dtmf(self, raw_config):
        dtmf_mode = raw_config.get(u'sip_dtmf_mode')
        if dtmf_mode in self._SIP_DTMF_MODE:
            raw_config[u'XX_out_of_band_dtmf'] = self._SIP_DTMF_MODE[dtmf_mode][0]
            raw_config[u'XX_dtmf_method'] = self._SIP_DTMF_MODE[dtmf_mode][1]

    def _add_locale(self, raw_config):
        locale = raw_config.get(u'locale')
        if locale in self._LOCALE:
            raw_config[u'XX_locale'] = self._LOCALE[locale]

    def _add_log_level(self, raw_config):
        syslog_level = raw_config.get(u'syslog_level')
        raw_config[u'XX_log_level'] = self._SYSLOG_LEVEL.get(syslog_level, u'1')

    def _add_transport_proto(self, raw_config):
        sip_transport = raw_config.get(u'sip_transport')
        if sip_transport in self._SIP_TRANSPORT:
            raw_config[u'XX_transport_proto'] = self._SIP_TRANSPORT[sip_transport]

    def _format_dst_change(self, suffix, dst_change):
        lines = []
        lines.append(u'dst %s month: %d' % (suffix, dst_change['month']))
        lines.append(u'dst %s hour: %d' % (suffix, min(dst_change['time'].as_hours, 23)))
        if dst_change['day'].startswith('D'):
            lines.append(u'dst %s day: %s' % (suffix, dst_change['day'][1:]))
        else:
            week, weekday = dst_change['day'][1:].split('.')
            if week == '5':
                lines.append(u'dst %s week: -1' % suffix)
            else:
                lines.append(u'dst %s week: %s' % (suffix, week))
            lines.append(u'dst %s day: %s' % (suffix, weekday))
        return lines

    def _format_tzinfo(self, tzinfo):
        lines = []
        lines.append(u'time zone name: Custom')
        lines.append(u'time zone minutes: %d' % -(tzinfo['utcoffset'].as_minutes))
        if tzinfo['dst'] is None:
            lines.append(u'dst config: 0')
        else:
            lines.append(u'dst config: 3')
            lines.append(u'dst minutes: %d' % (min(tzinfo['dst']['save'].as_minutes, 60)))
            if tzinfo['dst']['start']['day'].startswith('D'):
                lines.append(u'dst [start|end] relative date: 0')
            else:
                lines.append(u'dst [start|end] relative date: 1')
            lines.extend(self._format_dst_change('start', tzinfo['dst']['start']))
            lines.extend(self._format_dst_change('end', tzinfo['dst']['end']))
        return u'\n'.join(lines)

    def _add_timezone(self, raw_config):
        if u'timezone' in raw_config:
            try:
                tzinfo = tzinform.get_timezone_info(raw_config[u'timezone'])
            except tzinform.TimezoneNotFoundError, e:
                logger.info('Unknown timezone: %s', e)
            else:
                raw_config[u'XX_timezone'] = self._format_tzinfo(tzinfo)

    def _add_fkeys(self, raw_config, model):
        model_obj = self._MODELS.get(model)
        if not model_obj:
            logger.info('Unknown model %s; no function key will be configured', model)
            return
        lines = []
        for funckey_no, funckey_dict in sorted(raw_config[u'funckeys'].iteritems(),
                                               key=itemgetter(0)):
            keytype = model_obj.get_keytype(int(funckey_no))
            if keytype is None:
                logger.info('Function key %s is out of range for model %s', funckey_no, model)
                continue
            funckey_type = funckey_dict[u'type']
            if funckey_type == u'speeddial':
                type_ = u'speeddial'
                value = funckey_dict[u'value']
            elif funckey_type == u'blf':
                if keytype.startswith(u'softkey') and model.startswith(u'68'):
                    # 6800 series doesn't support the "blf" type on softkey
                    type_ = u'speeddial'
                else:
                    type_ = u'blf'
                value = funckey_dict[u'value']
            elif funckey_type == u'park':
                type_ = u'park'
                # note that value for park is ignored for firmware 3.x
                value = 'asterisk;%s' % funckey_dict[u'value']
            else:
                logger.info('Unsupported funckey type: %s', funckey_type)
                continue
            label = funckey_dict.get(u'label', value)
            line = funckey_dict.get(u'line', u'1')
            lines.append(u'%s type: %s' % (keytype, type_))
            lines.append(u'%s value: %s' % (keytype, value))
            lines.append(u'%s label: %s' % (keytype, label))
            lines.append(u'%s line: %s' % (keytype, line))
        raw_config[u'XX_fkeys'] = u'\n'.join(lines)

    def _update_sip_lines(self, raw_config):
        proxy_ip = raw_config.get(u'sip_proxy_ip')
        proxy_port = raw_config.get(u'sip_proxy_port', u'5060')
        backup_proxy_ip = raw_config.get(u'sip_backup_proxy_ip', u'0.0.0.0')
        backup_proxy_port = raw_config.get(u'sip_backup_proxy_port', u'5060')
        registrar_ip = raw_config.get(u'sip_registrar_ip')
        registrar_port = raw_config.get(u'sip_registrar_port', u'5060')
        backup_registrar_ip = raw_config.get(u'sip_backup_registrar_ip', u'0.0.0.0')
        backup_registrar_port = raw_config.get(u'sip_backup_registrar_port', u'5060')
        dtmf_mode = raw_config.get(u'sip_dtmf_mode')
        srtp_mode = raw_config.get(u'sip_srtp_mode')
        voicemail = raw_config.get(u'exten_voicemail')
        for line in raw_config[u'sip_lines'].itervalues():
            line.setdefault(u'proxy_ip', proxy_ip)
            line.setdefault(u'proxy_port', proxy_port)
            line.setdefault(u'backup_proxy_ip', backup_proxy_ip)
            line.setdefault(u'backup_proxy_port', backup_proxy_port)
            line.setdefault(u'registrar_ip', registrar_ip)
            line.setdefault(u'registrar_port', registrar_port)
            line.setdefault(u'backup_registrar_ip', backup_registrar_ip)
            line.setdefault(u'backup_registrar_port', backup_registrar_port)
            # add XX_dtmf_method
            cur_dtmf_mode = line.get(u'dtmf_mode', dtmf_mode)
            if cur_dtmf_mode in self._SIP_DTMF_MODE:
                line[u'XX_dtmf_method'] = self._SIP_DTMF_MODE[cur_dtmf_mode][1]
            else:
                line[u'XX_dtmf_method'] = u'0'
            # add XX_srtp_mode
            cur_srtp_mode = line.get(u'srtp_mode', srtp_mode)
            line[u'XX_srtp_mode'] = self._SIP_SRTP_MODE.get(cur_srtp_mode, u'0')
            # add voicemail
            if voicemail:
                line.setdefault(u'voicemail', voicemail)

    def _gen_xx_dict(self, raw_config):
        xx_dict = self._XX_DICT[self._XX_DICT_DEF]
        if u'locale' in raw_config:
            locale = raw_config[u'locale']
            lang = locale.split('_', 1)[0]
            if lang in self._XX_DICT:
                xx_dict = self._XX_DICT[lang]
        return xx_dict

    def _device_cert_or_key_filename(self, device, suffix):
        # Return the cert or key file filename for a device
        fmted_mac = format_mac(device[u'mac'], separator='', uppercase=True)
        return fmted_mac + suffix

    def _write_cert_or_key_file(self, pem_cert, device, suffix):
        filename = self._device_cert_or_key_filename(device, suffix)
        pathname = os.path.join(self._tftpboot_dir, filename)
        with open(pathname, 'w') as f:
            f.write(pem_cert)
        # return the path, from the point of view of the device
        return filename

    def _add_trusted_certificates(self, raw_config, device):
        if u'sip_servers_root_and_intermediate_certificates' in raw_config:
            pem_cert = raw_config[u'sip_servers_root_and_intermediate_certificates']
            raw_config[u'XX_trusted_certificates'] = self._write_cert_or_key_file(pem_cert, device,
                                                                    self._TRUSTED_ROOT_CERTS_SUFFIX)

    def _add_parking(self, raw_config):
        # hack to set the per line parking config if a park function key is used
        parking = None
        is_parking_set = False
        for funckey_no, funckey_dict in raw_config[u'funckeys'].iteritems():
            if funckey_dict[u'type'] == u'park':
                if is_parking_set:
                    cur_parking = funckey_dict[u'value']
                    if cur_parking != parking:
                        logger.warning('Ignoring park value %s for function key %s: using %s',
                                       cur_parking, funckey_no, parking)
                else:
                    parking = funckey_dict[u'value']
                    is_parking_set = True
                    self._do_add_parking(raw_config, parking)

    def _do_add_parking(self, raw_config, parking):
        raw_config[u'XX_parking'] = u'\n'.join(u'sip line%s park pickup config: %s;%s;asterisk' %
                                               (line_no, parking, parking)
                                               for line_no in raw_config[u'sip_lines'])

    def _add_xivo_phonebook_url(self, raw_config):
        if hasattr(plugins, 'add_xivo_phonebook_url') and raw_config.get(u'config_version', 0) >= 1:
            plugins.add_xivo_phonebook_url(raw_config, u'aastra')
        else:
            self._add_xivo_phonebook_url_compat(raw_config)

    def _add_xivo_phonebook_url_compat(self, raw_config):
        hostname = raw_config.get(u'X_xivo_phonebook_ip')
        if hostname:
            raw_config[u'XX_xivo_phonebook_url'] = u'http://{hostname}/service/ipbx/web_services.php/phonebook/search/'.format(hostname=hostname)

    _SENSITIVE_FILENAME_REGEX = re.compile(r'^[0-9A-F]{12}\.cfg$')

    def _dev_specific_filename(self, device):
        # Return the device specific filename (not pathname) of device
        fmted_mac = format_mac(device[u'mac'], separator='', uppercase=True)
        return fmted_mac + '.cfg'

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

        self._add_out_of_band_dtmf(raw_config)
        self._add_fkeys(raw_config, device.get(u'model'))
        self._add_locale(raw_config)
        self._add_log_level(raw_config)
        self._add_timezone(raw_config)
        self._add_transport_proto(raw_config)
        self._add_trusted_certificates(raw_config, device)
        self._update_sip_lines(raw_config)
        self._add_parking(raw_config)
        self._add_xivo_phonebook_url(raw_config)
        raw_config[u'XX_dict'] = self._gen_xx_dict(raw_config)
        raw_config[u'XX_options'] = device.get(u'options', {})
        raw_config[u'XX_language_path'] = self._LANGUAGE_PATH

        path = os.path.join(self._tftpboot_dir, filename)
        self._tpl_helper.dump(tpl, raw_config, path, self._ENCODING)

    def deconfigure(self, device):
        self._remove_configuration_file(device)
        self._remove_certificate_file(device)

    def _remove_configuration_file(self, device):
        path = os.path.join(self._tftpboot_dir, self._dev_specific_filename(device))
        try:
            os.remove(path)
        except OSError as e:
            logger.info('error while removing configuration file: %s', e)

    def _remove_certificate_file(self, device):
        path = os.path.join(self._tftpboot_dir,
                            self._device_cert_or_key_filename(device, self._TRUSTED_ROOT_CERTS_SUFFIX))
        try:
            os.remove(path)
        except OSError as e:
            if e.errno != errno.ENOENT:
                logger.info('error while removing certificate file: %s', e)

    if hasattr(synchronize, 'standard_sip_synchronize'):
        def synchronize(self, device, raw_config):
            return synchronize.standard_sip_synchronize(device)

    else:
        # backward compatibility with older wazo-provd server
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

    def get_remote_state_trigger_filename(self, device):
        if u'mac' not in device:
            return None

        return self._dev_specific_filename(device)

    def is_sensitive_filename(self, filename):
        return bool(self._SENSITIVE_FILENAME_REGEX.match(filename))
