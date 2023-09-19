# Copyright 2021-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later
from textwrap import dedent
import pytest
from unittest.mock import MagicMock, patch, sentinel
from provd.devices.config import RawConfigError
from provd.devices.pgasso import DeviceSupport
from provd.tzinform import TimezoneNotFoundError

from ..common import (
    BaseYealinkHTTPDeviceInfoExtractor,
    BaseYealinkPgAssociator,
)

TEST_LINES = """\
linekey.1.type = 13
linekey.1.line = 1
linekey.1.value = test_speed_dial
linekey.1.label = Test Speed dial

linekey.2.type = 16
linekey.2.line = 1
linekey.2.value = test_blf
linekey.2.label = Test blf
linekey.2.extension = 1234

linekey.3.type = 10
linekey.3.line = 1
linekey.3.value = test_park
linekey.3.label = Test Park

"""


class TestInfoExtraction:
    @classmethod
    def setup_class(cls):
        cls.http_info_extractor = BaseYealinkHTTPDeviceInfoExtractor()

    def _mock_request(self, ua: bytes = None, path: bytes = None):
        request = MagicMock()
        request.getHeader = MagicMock(return_value=ua)
        request.path = path
        return request

    def test_http_ua_extractor_when_all_info(self):
        ua_info = {
            b'Yealink SIP-T20P 9.72.0.30 00:15:65:5e:16:7c': {
                'vendor': 'Yealink',
                'model': 'T20P',
                'version': '9.72.0.30',
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

    @patch('v86.common.defer')
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
            b'/001565123456.cfg': '00:15:65:12:34:56',
            b'/e434d7123456.cfg': 'e4:34:d7:12:34:56',
            b'/805ec0123456.cfg': '80:5e:c0:12:34:56',
            b'/805e0c123456.cfg': '80:5e:0c:12:34:56',
            b'/249ad8123456.cfg': '24:9a:d8:12:34:56',
        }

        for path, mac in macs_from_paths.items():
            result = self.http_info_extractor._do_extract(self._mock_request(path=path))
            if result is None:
                raise Exception(path, mac)
            assert {'vendor': 'Yealink', 'mac': mac}.items() <= result.items()

    @patch('v86.common.logger')
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
        request.path = b'/e434d7jabd'
        self.http_info_extractor._extract_from_path(request)
        message, mac, exception = mocked_logger.warning.call_args[0]
        assert message == 'Could not normalize MAC address "%s": %s'
        assert mac == b'e434d7'
        assert isinstance(exception, ValueError)
        assert str(exception) == 'invalid MAC string'


class TestPluginAssociation:
    def test_plugin_association_when_all_info_match(self, v86_entry):
        plugin_associator = BaseYealinkPgAssociator(v86_entry.MODEL_VERSIONS)
        for model, version in v86_entry.MODEL_VERSIONS.items():
            support = plugin_associator._do_associate('Yealink', model, version)
            assert support == DeviceSupport.EXACT

    def test_plugin_association_when_only_vendor_and_model_match(self, v86_entry):
        plugin_associator = BaseYealinkPgAssociator(v86_entry.MODEL_VERSIONS)
        for model in v86_entry.MODEL_VERSIONS:
            support = plugin_associator._do_associate('Yealink', model, None)
            assert support == DeviceSupport.COMPLETE

    def test_plugin_association_when_only_vendor_matches(self, v86_entry):
        plugin_associator = BaseYealinkPgAssociator(v86_entry.MODEL_VERSIONS)
        support = plugin_associator._do_associate('Yealink', None, None)
        assert support == DeviceSupport.PROBABLE

    def test_plugin_association_when_nothing_matches(self, v86_entry):
        plugin_associator = BaseYealinkPgAssociator(v86_entry.MODEL_VERSIONS)
        support = plugin_associator._do_associate(
            'DoesNotMatch', 'NothingPhone', '1.2.3'
        )
        assert support == DeviceSupport.IMPROBABLE

    def test_plugin_association_does_not_match_when_empty_strings(self, v86_entry):
        plugin_associator = BaseYealinkPgAssociator(v86_entry.MODEL_VERSIONS)
        assert plugin_associator._do_associate('', '', '') == DeviceSupport.IMPROBABLE


class TestPlugin:
    @patch('v86.common.FetchfwPluginHelper')
    def test_init(self, fetch_fw, v86_entry):
        fetch_fw.return_value.services.return_value = sentinel.fetchfw_services
        fetch_fw.new_downloaders.return_value = sentinel.fetchfw_downloaders
        plugin = v86_entry.YealinkPlugin(
            MagicMock(), 'test_dir', MagicMock(), MagicMock()
        )
        assert plugin.services == sentinel.fetchfw_services
        fetch_fw.assert_called_once_with('test_dir', sentinel.fetchfw_downloaders)

    def test_common_configure(self, v86_plugin):
        raw_config = {}
        v86_plugin._tpl_helper.get_template.return_value = 'template'
        v86_plugin.configure_common(raw_config)
        v86_plugin._tpl_helper.get_template.assert_called_with('common/dect_model.tpl')
        assert len(v86_plugin._tpl_helper.dump.mock_calls) == 15

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
            'sip_lines': {'1': {'number': '5888'}},
            'http_base_url': 'http://localhost:8667',
        }
        v86_plugin._tpl_helper.get_dev_template.return_value = 'template'
        v86_plugin.configure(device, raw_config)
        v86_plugin._tpl_helper.get_dev_template.assert_called_with(
            '805ec0d57d72.cfg', device
        )
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
        message, exception = mocked_logger.info.call_args[0]
        assert message == 'error while removing file: %s'
        assert isinstance(exception, FileNotFoundError)

    @patch('v86.common.synchronize')
    def test_synchronize(self, provd_synchronize, v86_plugin):
        device = {'mac': '80:5e:c0:d5:7d:72'}
        v86_plugin.synchronize(device, {})
        provd_synchronize.standard_sip_synchronize.assert_called_with(device)

    def test_get_remote_state_trigger_filename(self, v86_plugin):
        assert v86_plugin.get_remote_state_trigger_filename({}) is None
        assert (
            v86_plugin.get_remote_state_trigger_filename({'mac': '80:5e:c0:d5:7d:72'})
            == '805ec0d57d72.cfg'
        )

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
        raw_config = {'config_version': 1}
        v86_plugin._add_xivo_phonebook_url(raw_config)
        provd_plugins.add_xivo_phonebook_url.assert_called_with(
            raw_config,
            'yealink',
            entry_point='lookup',
            qs_suffix='term=#SEARCH',
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
            },
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
                'XX_template_id': 5,
            },
            '2': None,
            '3': None,
            '4': None,
        }

    @patch('v86.common.logger')
    def test_timezones(self, mocked_logger, v86_plugin):
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
        raw_config = {'timezone': 'Asia/Tehran'}
        v86_plugin._add_timezone(raw_config)
        assert raw_config['XX_timezone'] == dedent(
            """\
            local_time.time_zone = +3
            local_time.summer_time = 1
            local_time.dst_time_type = 0
            local_time.start_time = 03/22/00
            local_time.end_time = 09/22/00
            local_time.offset_time = 60"""
        )
        v86_plugin._add_timezone({'timezone': 'Doesnt/Exist'})
        message, exception = mocked_logger.warning.call_args[0]
        assert message == 'Unknown timezone: %s'
        assert isinstance(exception, TimezoneNotFoundError)

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
            'sip_lines': {'1': {'number': '5888'}},
            'exten_pickup_call': '1234',
        }
        v86_plugin._add_fkeys({'model': 'T32G'}, raw_config)
        assert raw_config['XX_fkeys'] == ''
        v86_plugin._add_fkeys({'model': 'T33G'}, raw_config)
        mocked_logger.info.assert_called_with('Unsupported funckey type: %s', 'other')
        assert raw_config['XX_fkeys'] == TEST_LINES + self._build_fkey_expectation(
            4, 12
        )

    def _build_fkey_expectation(self, start_line, end_line):
        return '\n'.join(
            [
                dedent(
                    '''\
               linekey.{line}.type = 0
               linekey.{line}.line = %NULL%
               linekey.{line}.value = %NULL%
               linekey.{line}.label = %NULL%
           '''
                ).format(line=line)
                for line in range(start_line, end_line + 1)
            ]
        )

    def _build_exp_expectation(self, start_line, end_line, expansion_number):
        return '\n'.join(
            [
                dedent(
                    '''\
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
                    '''\
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

    def test_fkeys_with_exp40(self, v86_plugin):
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
        v86_plugin._add_fkeys({'model': 'T27G'}, raw_config)
        assert raw_config['XX_fkeys'] == TEST_LINES + self._build_exp_expectation(
            4, 21, 40
        )
        raw_config = dict(**base_raw_config)
        v86_plugin._add_fkeys({'model': 'T5'}, raw_config)
