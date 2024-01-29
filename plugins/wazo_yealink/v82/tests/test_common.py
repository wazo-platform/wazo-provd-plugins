# Copyright 2021-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

from textwrap import dedent
from unittest.mock import MagicMock, patch, sentinel

import pytest
from wazo_provd.devices.config import RawConfigError
from wazo_provd.devices.pgasso import DeviceSupport
from wazo_provd.tzinform import TimezoneNotFoundError

from ..common import BaseYealinkHTTPDeviceInfoExtractor, BaseYealinkPgAssociator

BASE_TEST_LINES = """\
linekey.1.type = 13
linekey.1.line = 1
linekey.1.value = test_speed_dial
linekey.1.label = Test Speed dial

linekey.2.type = 16
linekey.2.line = 1
linekey.2.value = test_blf
linekey.2.label = Test blf
linekey.2.pickup_value = 1234
linekey.2.extension = 1234
"""

TEST_LINES = (
    BASE_TEST_LINES
    + """
linekey.3.type = 10
linekey.3.line = 1
linekey.3.value = test_park
linekey.3.label = Test Park
"""
)


class TestInfoExtraction:
    http_info_extractor: BaseYealinkHTTPDeviceInfoExtractor

    @classmethod
    def setup_class(cls):
        cls.http_info_extractor = BaseYealinkHTTPDeviceInfoExtractor()

    def _mock_request(self, ua: bytes | None = None, path: bytes | None = None):
        request = MagicMock()
        request.getHeader = MagicMock(return_value=ua)
        request.path = path
        return request

    def test_http_ua_extractor_when_all_info(self):
        ua_info = {
            b'Yealink SIP-CP920 78.85.0.5 00:15:65:5e:16:7c': {
                'vendor': 'Yealink',
                'model': 'CP920',
                'version': '78.85.0.5',
                'mac': '00:15:65:5e:16:7c',
            },
            b'Yealink SIP-T31G 124.85.257.55 80:5e:c0:d5:7d:72': {
                'vendor': 'Yealink',
                'model': 'T31G',
                'version': '124.85.257.55',
                'mac': '80:5e:c0:d5:7d:72',
            },
        }

        for ua, info in ua_info.items():
            result = self.http_info_extractor._do_extract(self._mock_request(ua=ua))
            assert info.items() <= result.items()

    def test_http_ua_extractor_when_no_info(self):
        assert self.http_info_extractor._extract_from_ua('') is None

    @patch('plugins.wazo_yealink.v82.common.defer')
    def test_extract(self, mocked_defer):
        self.http_info_extractor.extract(
            self._mock_request(b'Yealink SIP-T31G 124.85.257.55 80:5e:c0:d5:7d:72'),
            None,
        )
        mocked_defer.succeed.assert_called_with(
            {
                'mac': '80:5e:c0:d5:7d:72',
                'version': '124.85.257.55',
                'vendor': 'Yealink',
                'model': 'T31G',
            }
        )

    def test_http_extractor_when_no_ua_extracts_mac_from_path(self):
        macs_from_paths = {
            b'/0015654c4c26.cfg': '00:15:65:4c:4c:26',
            b'/0015655e167c.cfg': '00:15:65:5e:16:7c',
            b'/0015654b57d2.cfg': '00:15:65:4b:57:d2',
            b'/0015658c4812.cfg': '00:15:65:8c:48:12',
        }

        for path, mac in macs_from_paths.items():
            assert self.http_info_extractor._do_extract(
                self._mock_request(path=path)
            ) == {'mac': mac}

        assert self.http_info_extractor._do_extract(
            self._mock_request(path=b'/y000000000025.cfg')
        ) == {'vendor': 'Yealink', 'model': 'W52P'}

    @patch('plugins.wazo_yealink.v82.common.logger')
    def test_invalid_mac(self, mocked_logger):
        self.http_info_extractor._extract_from_ua(
            'Yealink SIP-T20P 9.72.0.30 00:15:6525ef16a7c'
        )
        message, mac, exception = mocked_logger.warning.call_args[0]
        assert message == 'Could not normalize MAC address "%s": %s'
        assert mac == '00:15:6525ef16a7c'
        assert isinstance(exception, ValueError)
        assert str(exception) == 'invalid MAC string'

        mocked_logger.reset_mock()
        request = MagicMock()
        request.path = b'/001565jabd'
        self.http_info_extractor._extract_from_path(request)
        message, mac, exception = mocked_logger.warning.call_args[0]
        assert message == 'Could not normalize MAC address "%s": %s'
        assert mac == b'001565'
        assert isinstance(exception, ValueError)
        assert str(exception) == 'invalid MAC string'


class TestPluginAssociation:
    def test_plugin_association_when_all_info_match(self, v82_entry):
        plugin_associator = BaseYealinkPgAssociator(v82_entry.MODEL_INFO)
        for model, info in v82_entry.MODEL_INFO.items():
            assert (
                plugin_associator._do_associate('Yealink', model, info['version'])
                == DeviceSupport.EXACT
            )

    def test_plugin_association_when_only_vendor_and_model_match(self, v82_entry):
        plugin_associator = BaseYealinkPgAssociator(v82_entry.MODEL_INFO)
        for model in v82_entry.MODEL_INFO:
            assert (
                plugin_associator._do_associate('Yealink', model, None)
                == DeviceSupport.COMPLETE
            )

    def test_plugin_association_when_only_vendor_matches(self, v82_entry):
        plugin_associator = BaseYealinkPgAssociator(v82_entry.MODEL_INFO)
        assert (
            plugin_associator._do_associate('Yealink', None, None)
            == DeviceSupport.PROBABLE
        )

    def test_plugin_association_when_nothing_matches(self, v82_entry):
        plugin_associator = BaseYealinkPgAssociator(v82_entry.MODEL_INFO)
        assert (
            plugin_associator._do_associate('DoesNotMatch', 'NothingPhone', '1.2.3')
            == DeviceSupport.IMPROBABLE
        )

    def test_plugin_association_does_not_match_when_empty_strings(self, v82_entry):
        plugin_associator = BaseYealinkPgAssociator(v82_entry.MODEL_INFO)
        assert plugin_associator._do_associate('', '', '') == DeviceSupport.IMPROBABLE


class TestPlugin:
    @patch('plugins.wazo_yealink.v82.common.FetchfwPluginHelper')
    def test_init(self, fetch_fw, v82_entry):
        fetch_fw.return_value.services.return_value = sentinel.fetchfw_services
        fetch_fw.new_downloaders.return_value = sentinel.fetchfw_downloaders
        plugin = v82_entry.YealinkPlugin(
            MagicMock(), 'test_dir', MagicMock(), MagicMock()
        )
        assert plugin.services == sentinel.fetchfw_services
        fetch_fw.assert_called_once_with('test_dir', sentinel.fetchfw_downloaders)

    def test_configure(self, v82_plugin):
        device = {
            'vendor': 'Yealink',
            'model': 'T23P',
            'version': '124.85.257.55',
            'mac': '80:5e:c0:d5:7d:72',
        }
        raw_config = {
            'http_port': '80',
            'locale': 'en_US',
            'funckeys': {},
            'sip_proxy_ip': '1.1.1.1',
            'sip_lines': {'1': {'number': '5888'}},
            'http_base_url': 'http://localhost:8667',
        }
        v82_plugin._tpl_helper.get_dev_template.return_value = 'template'
        v82_plugin.configure(device, raw_config)
        v82_plugin._tpl_helper.get_dev_template.assert_called_with(
            '805ec0d57d72.cfg', device
        )
        v82_plugin._tpl_helper.dump.assert_called_with(
            'template', raw_config, 'test_dir/var/tftpboot/805ec0d57d72.cfg', 'UTF-8'
        )

    @patch('os.remove')
    def test_deconfigure(self, mocked_remove, v82_plugin):
        v82_plugin.deconfigure({'mac': '80:5e:c0:d5:7d:72'})
        mocked_remove.assert_called_with('test_dir/var/tftpboot/805ec0d57d72.cfg')

    @patch('plugins.wazo_yealink.v82.common.logger')
    def test_deconfigure_no_file(self, mocked_logger, v82_plugin):
        v82_plugin.deconfigure({'mac': '00:00:00:00:00:00'})
        message, exception = mocked_logger.info.call_args[0]
        assert message == 'error while removing file: %s'
        assert isinstance(exception, FileNotFoundError)

    @patch('plugins.wazo_yealink.v82.common.synchronize')
    def test_synchronize(self, provd_synchronize, v82_plugin):
        device = {'mac': '80:5e:c0:d5:7d:72'}
        v82_plugin.synchronize(device, {})
        provd_synchronize.standard_sip_synchronize.assert_called_with(device)

    def test_get_remote_state_trigger_filename(self, v82_plugin):
        assert v82_plugin.get_remote_state_trigger_filename({}) is None
        assert (
            v82_plugin.get_remote_state_trigger_filename({'mac': '80:5e:c0:d5:7d:72'})
            == '805ec0d57d72.cfg'
        )

    def test_sensitive_file(self, v82_plugin):
        assert v82_plugin.is_sensitive_filename('patate') is False
        assert v82_plugin.is_sensitive_filename('805ec0d57d72.cfg') is True

    def test_add_country_and_lang(self, v82_plugin):
        raw_config = {'locale': 'en_US'}
        v82_plugin._add_country_and_lang(raw_config)
        assert raw_config['XX_country'] == 'United States'
        assert raw_config['XX_lang'] == 'English'
        assert raw_config['XX_handset_lang'] == '0'
        raw_config = {'locale': 'ja_JP'}
        v82_plugin._add_country_and_lang(raw_config)
        assert raw_config == {'locale': 'ja_JP'}

    def test_checks(self, v82_plugin):
        with pytest.raises(RawConfigError):
            v82_plugin._check_config({})

        with pytest.raises(Exception):
            v82_plugin._check_device({})

    @patch('plugins.wazo_yealink.v82.common.plugins')
    def test_phonebook_url(self, provd_plugins, v82_plugin):
        raw_config = {'config_version': 1}
        v82_plugin._add_xivo_phonebook_url(raw_config)
        provd_plugins.add_xivo_phonebook_url.assert_called_with(
            raw_config,
            'yealink',
            entry_point='lookup',
            qs_suffix='term=#SEARCH',
        )

    def test_sip_lines(self, v82_plugin):
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
            },
        }
        v82_plugin._add_xx_sip_lines({'model': 'patate'}, raw_config)
        assert raw_config['sip_lines'] == raw_config['XX_sip_lines']

        v82_plugin._update_sip_lines(raw_config)
        v82_plugin._add_xx_sip_lines({'model': 'T23G'}, raw_config)
        assert raw_config['XX_sip_lines'] == {
            '1': {
                'number': '5888',
                'XX_line_no': 1,
                'XX_dtmf_type': '2',
                'voicemail': '*98',
                'proxy_ip': '1.1.1.1',
                'proxy_port': '5080',
            },
            '2': None,
            '3': None,
        }

    @patch('plugins.wazo_yealink.v82.common.logger')
    def test_timezones(self, mocked_logger, v82_plugin):
        raw_config = {'timezone': 'America/Montreal'}
        v82_plugin._add_timezone(raw_config)
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
        v82_plugin._add_timezone(raw_config)
        assert raw_config['XX_timezone'] == dedent(
            """\
            local_time.time_zone = -6
            local_time.summer_time = 0"""
        )
        raw_config = {'timezone': 'Asia/Tehran'}
        v82_plugin._add_timezone(raw_config)
        assert raw_config['XX_timezone'] == dedent(
            """\
            local_time.time_zone = +3
            local_time.summer_time = 1
            local_time.dst_time_type = 0
            local_time.start_time = 03/22/00
            local_time.end_time = 09/22/00
            local_time.offset_time = 60"""
        )
        v82_plugin._add_timezone({'timezone': 'Doesnt/Exist'})
        message, exception = mocked_logger.warning.call_args[0]
        assert message == 'Unknown timezone: %s'
        assert isinstance(exception, TimezoneNotFoundError)

    @patch('plugins.wazo_yealink.v82.common.logger')
    def test_function_keys(self, mocked_logger, v82_plugin):
        raw_config = {
            'funckeys': {
                '1': {
                    'type': 'speeddial',
                    'value': 'test_speed_dial',
                    'label': 'Test Speed dial',
                },
                '3': {
                    'type': 'other',
                    'value': 'test',
                },
                '2': {
                    'type': 'blf',
                    'value': 'test_blf',
                    'label': 'Test blf',
                },
            },
            'sip_lines': {'1': {'number': '5888'}},
            'exten_pickup_call': '1234',
        }
        v82_plugin._add_fkeys({'model': 'ABC'}, raw_config)
        mocked_logger.info.assert_called_with(
            'Unknown model %s; no memorykey will be configured', 'ABC'
        )
        mocked_logger.reset_mock()
        assert raw_config['XX_fkeys'] == ''
        v82_plugin._add_fkeys({'model': 'T40P'}, raw_config)
        mocked_logger.info.assert_called_with('Unsupported funckey type: %s', 'other')
        assert raw_config['XX_fkeys'] == BASE_TEST_LINES + '\n'

    def _build_exp_expectation(self, start_line, end_line, expansion_number):
        return ''.join(
            [
                dedent(
                    '''
               linekey.{line}.type = 0
               linekey.{line}.line = %NULL%
               linekey.{line}.value = %NULL%
               linekey.{line}.label = %NULL%
           '''
                ).format(line=line)
                for line in range(start_line, end_line + 1)
            ]
            + [
                dedent(
                    '''
                expansion_module.{page}.key.{key}.type = 0
                expansion_module.{page}.key.{key}.line = %NULL%
                expansion_module.{page}.key.{key}.value = %NULL%
                expansion_module.{page}.key.{key}.label = %NULL%
            '''
                ).format(key=key, page=page)
                for page in range(1, 7)
                for key in range(1, expansion_number + 1)
            ]
        )

    def test_fkeys_with_exp40(self, v82_plugin):
        base_raw_config = {
            'funckeys': {
                '1': {
                    'type': 'speeddial',
                    'value': 'test_speed_dial',
                    'label': 'Test Speed dial',
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
            'sip_lines': {'1': {'number': '5888'}},
            'exten_pickup_call': '1234',
        }
        raw_config = dict(**base_raw_config)
        v82_plugin._add_fkeys({'model': 'T27G'}, raw_config)
        assert raw_config['XX_fkeys'] == TEST_LINES + self._build_exp_expectation(
            4, 21, 40
        )
        raw_config = dict(**base_raw_config)
        v82_plugin._add_fkeys({'model': 'T5'}, raw_config)
