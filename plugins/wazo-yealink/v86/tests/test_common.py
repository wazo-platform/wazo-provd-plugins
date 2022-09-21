# -*- coding: utf-8 -*-

# Copyright 2021-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import
from __future__ import unicode_literals

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = OSError

from textwrap import dedent

import pytest
import six

from hamcrest import (
    assert_that,
    equal_to,
    has_entries,
    has_properties,
)
from mock import MagicMock, patch, sentinel
from provd.devices.config import RawConfigError
from provd.devices.pgasso import (
    COMPLETE_SUPPORT,
    FULL_SUPPORT,
    IMPROBABLE_SUPPORT,
    PROBABLE_SUPPORT,
)
from ..common import (
    BaseYealinkHTTPDeviceInfoExtractor,
    BaseYealinkPgAssociator,
)
from ..models import MODEL_VERSIONS


class TestInfoExtraction(object):
    @classmethod
    def setup_class(cls):
        cls.http_info_extractor = BaseYealinkHTTPDeviceInfoExtractor()

    def _mock_request(self, ua=None, path=None):
        request = MagicMock()
        request.getHeader = MagicMock(return_value=ua)
        request.path = path
        return request

    def test_http_ua_extractor_when_all_info(self):
        ua_infos = {
            'Yealink SIP-T20P 9.72.0.30 00:15:65:5e:16:7c': {
                'vendor': 'Yealink',
                'model': 'T20P',
                'version': '9.72.0.30',
                'mac': '00:15:65:5e:16:7c',
            },
            'Yealink SIP-T31G 124.85.257.55 80:5e:c0:d5:7d:72': {
                'vendor': 'Yealink',
                'model': 'T31G',
                'version': '124.85.257.55',
                'mac': '80:5e:c0:d5:7d:72',
            },
        }

        for ua, info in ua_infos.items():
            assert_that(
                self.http_info_extractor._do_extract(self._mock_request(ua=ua)),
                has_entries(info),
            )

    def test_http_extractor_when_no_ua_extracts_mac_from_path(self):
        macs_from_paths = {
            '/001565123456.cfg': '00:15:65:12:34:56',
            '/e434d7123456.cfg': 'e4:34:d7:12:34:56',
            '/805ec0123456.cfg': '80:5e:c0:12:34:56',
            '/805e0c123456.cfg': '80:5e:0c:12:34:56',
            '/249ad8123456.cfg': '24:9a:d8:12:34:56',
        }

        for path, mac in six.iteritems(macs_from_paths):
            assert_that(
                self.http_info_extractor._do_extract(self._mock_request(path=path)),
                has_entries({u'vendor': u'Yealink', u'mac': mac}),
            )

    @patch('v86.common.logger')
    def test_invalid_mac(self, mocked_logger):
        self.http_info_extractor._extract_from_ua('Yealink SIP-T20P 9.72.0.30 00:15:6525ef16a7c')
        message, mac, exception = mocked_logger.warning.call_args.args
        assert message == 'Could not normalize MAC address "%s": %s'
        assert mac == '00:15:6525ef16a7c'
        assert isinstance(exception, ValueError)
        assert str(exception) == 'invalid MAC string'

        mocked_logger.reset_mock()
        request = MagicMock()
        request.path = '/e434d7jabd'
        self.http_info_extractor._extract_from_path(request)
        message, mac, exception = mocked_logger.warning.call_args.args
        assert message == 'Could not normalize MAC address "%s": %s'
        assert mac == 'e434d7'
        assert isinstance(exception, ValueError)
        assert str(exception) == 'invalid MAC string'


class TestPluginAssociation(object):
    @classmethod
    def setup_class(cls):
        cls.plugin_associator = BaseYealinkPgAssociator(MODEL_VERSIONS)

    def test_plugin_association_when_all_info_match(self):
        for model, version in six.iteritems(MODEL_VERSIONS):
            assert_that(
                self.plugin_associator._do_associate('Yealink', model, version),
                equal_to(FULL_SUPPORT),
            )

    def test_plugin_association_when_only_vendor_and_model_match(self):
        for model in six.iterkeys(MODEL_VERSIONS):
            assert_that(
                self.plugin_associator._do_associate('Yealink', model, None),
                equal_to(COMPLETE_SUPPORT),
            )

    def test_plugin_association_when_only_vendor_matches(self):
        assert_that(
            self.plugin_associator._do_associate('Yealink', None, None),
            equal_to(PROBABLE_SUPPORT),
        )

    def test_plugin_association_when_nothing_matches(self):
        assert_that(
            self.plugin_associator._do_associate('DoesNotMatch', 'NothingPhone', '1.2.3'),
            equal_to(IMPROBABLE_SUPPORT),
        )

    def test_plugin_association_does_not_match_when_empty_strings(self):
        assert_that(
            self.plugin_associator._do_associate('', '', ''),
            equal_to(IMPROBABLE_SUPPORT),
        )


class TestPlugin(object):
    @patch('v86.common.FetchfwPluginHelper')
    def test_init(self, fetch_fw, v86_entry):
        fetch_fw.return_value.services.return_value = sentinel.fetchfw_services
        fetch_fw.new_downloaders.return_value = sentinel.fetchfw_downloaders
        plugin = v86_entry.YealinkPlugin(MagicMock(), 'test_dir', MagicMock(), MagicMock())
        assert_that(
            plugin,
            has_properties(
                services=sentinel.fetchfw_services,
            ),
        )
        fetch_fw.assert_called_once_with('test_dir', sentinel.fetchfw_downloaders)

    def test_common_configure(self, v86_plugin):
        raw_config = {}
        v86_plugin._tpl_helper.get_template.return_value = 'template'
        v86_plugin.configure_common(raw_config)
        v86_plugin._tpl_helper.get_template.assert_called_with('common/dect_model.tpl')
        assert len(v86_plugin._tpl_helper.dump.mock_calls) == 14

    def test_configure(self, v86_plugin):
        device = {
            'vendor': 'Yealink',
            'model': 'T31G',
            'version': '124.85.257.55',
            'mac': '80:5e:c0:d5:7d:72',
        }
        raw_config = {
            'http_port': '80',
            'locale': 'en_US',
            'funckeys': {},
            'sip_proxy_ip': '1.1.1.1',
            'sip_lines': {'1': {'number': '5888'}}
        }
        v86_plugin._tpl_helper.get_dev_template.return_value = 'template'
        v86_plugin.configure(device, raw_config)
        v86_plugin._tpl_helper.get_dev_template.assert_called_with('805ec0d57d72.cfg', device)
        v86_plugin._tpl_helper.dump.assert_called_with(
            'template', raw_config, 'test_dir/var/tftpboot/805ec0d57d72.cfg', 'UTF-8'
        )

    @patch('os.remove')
    def test_deconfigure(self, mocked_remove, v86_plugin):
        v86_plugin.deconfigure({'mac': '80:5e:c0:d5:7d:72'})
        mocked_remove.assert_called_with('test_dir/var/tftpboot/805ec0d57d72.cfg')

    @patch('v86.common.logger')
    def test_deconfigure_no_file(self, mocked_logger, v86_plugin):
        v86_plugin.deconfigure({'mac': '00:00:00:00:00:00'})
        message, exception = mocked_logger.info.call_args.args
        assert message == 'error while removing file: %s'
        assert isinstance(exception, FileNotFoundError)

    def test_sensitive_file(self, v86_plugin):
        assert v86_plugin.is_sensitive_filename('patate') is False
        assert v86_plugin.is_sensitive_filename('805ec0d57d72.cfg') is True

    def test_add_country_and_lang(self, v86_plugin):
        raw_config = {'locale': 'en_US'}
        v86_plugin._add_country_and_lang(raw_config)
        assert raw_config['XX_country'] == 'United States'
        assert raw_config['XX_lang'] == 'English'
        assert raw_config['XX_handset_lang'] == '0'
        raw_config = {'locale': 'ja_JP'}
        v86_plugin._add_country_and_lang(raw_config)
        assert raw_config == {'locale': 'ja_JP'}

    def test_checks(self, v86_plugin):
        with pytest.raises(RawConfigError):
            v86_plugin._check_config({})

        with pytest.raises(Exception):
            v86_plugin._check_device({})

    @patch('v86.common.plugins')
    def test_phonebook_url(self, provd_plugins, v86_plugin):
        raw_config = {
            'config_version': 0,
            'X_xivo_phonebook_ip': '1.1.1.1',
        }
        v86_plugin._add_xivo_phonebook_url(raw_config)
        provd_plugins.add_xivo_phonebook_url.assert_not_called()
        expected_url = 'http://1.1.1.1/service/ipbx/web_services.php/phonebook/search/?name=#SEARCH'
        assert raw_config['XX_xivo_phonebook_url'] == expected_url

        raw_config = {'config_version': 1}
        v86_plugin._add_xivo_phonebook_url(raw_config)
        provd_plugins.add_xivo_phonebook_url.assert_called_with(
            raw_config, 'yealink', entry_point='lookup', qs_suffix='term=#SEARCH',
        )

    def test_sip_lines(self, v86_plugin):
        raw_config = {
            'sip_dtmf_mode': 'SIP-INFO',
            'exten_voicemail': '*98',
            'sip_proxy_ip': '1.1.1.1',
            'sip_proxy_port': '5080',
            'XX_templates': {('1.1.1.1', '5080'): {'id': 5}},
            'sip_lines': {
                '1': {
                    'number': '5888',
                }
            }
        }
        v86_plugin._add_xx_sip_lines({'model': 'patate'}, raw_config)
        assert raw_config['sip_lines'] == raw_config['XX_sip_lines']

        v86_plugin._update_sip_lines(raw_config)
        v86_plugin._add_xx_sip_lines({'model': 'T33G'}, raw_config)
        assert raw_config['XX_sip_lines'] == {
            '1': {
                'number': '5888',
                'XX_line_no': 1,
                'XX_dtmf_type': '2',
                'voicemail': '*98',
                'proxy_ip': '1.1.1.1',
                'proxy_port': '5080',
                'XX_template_id': 5
            },
            '2': None,
            '3': None,
            '4': None,
        }

    def test_timezones(self, v86_plugin):
        raw_config = {'timezone': 'America/Montreal'}
        v86_plugin._add_timezone(raw_config)
        assert raw_config['XX_timezone'] == dedent(
            """\
            local_time.time_zone = -5
            local_time.summer_time = 1
            local_time.dst_time_type = 1
            local_time.start_time = 3/2/7/2
            local_time.end_time = 11/1/7/2
            local_time.offset_time = 60"""
        )
        raw_config = {'timezone': 'America/Regina'}
        v86_plugin._add_timezone(raw_config)
        assert raw_config['XX_timezone'] == dedent(
            """\
            local_time.time_zone = -6
            local_time.summer_time = 0"""
        )

    @patch('v86.common.logger')
    def test_function_keys(self, mocked_logger, v86_plugin):
        raw_config = {
            'funckeys': {
                '1': {
                    'type': 'speeddial',
                    'value': 'test_speed_dial',
                    'label': 'Test Speed dial',
                },
                '4': {
                    'type': 'other',
                    'value': 'test',
                },
                '2': {
                    'type': 'blf',
                    'value': 'test_blf',
                    'label': 'Test blf',
                },
                '3': {
                    'type': 'park',
                    'value': 'test_park',
                    'label': 'Test Park',
                },
            },
            'sip_lines': {
                '1': {'number': '5888'}
            }
        }
        v86_plugin._add_fkeys({'model': 'T33G'}, raw_config)
        mocked_logger.info.assert_called_with('Unsupported funckey type: %s', 'other')
        assert raw_config['XX_fkeys'] == dedent(
            """\
            linekey.1.type = 13
            linekey.1.line = 1
            linekey.1.value = test_speed_dial
            linekey.1.label = Test Speed dial
           
            linekey.2.type = 16
            linekey.2.line = 1
            linekey.2.value = test_blf
            linekey.2.label = Test blf
            
            linekey.3.type = 10
            linekey.3.line = 1
            linekey.3.value = test_park
            linekey.3.label = Test Park
            
            """
        )
