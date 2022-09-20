# -*- coding: utf-8 -*-

# Copyright 2021-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import
from __future__ import unicode_literals

import six
import pytest

from hamcrest import (
    assert_that,
    equal_to,
    has_entries,
    has_properties,
)
from mock import MagicMock, patch, sentinel
from provd.devices.pgasso import (
    COMPLETE_SUPPORT,
    FULL_SUPPORT,
    IMPROBABLE_SUPPORT,
    PROBABLE_SUPPORT,
)
from ..common import (
    BaseYealinkHTTPDeviceInfoExtractor,
    BaseYealinkPgAssociator,
    BaseYealinkPlugin,
)
from ..models import MODEL_VERSIONS


@pytest.fixture(name='v86_entry')
def v86_entry_fixture(module_initializer):
    def execfile_(_, common_globals):
        common_globals['BaseYealinkPlugin'] = BaseYealinkPlugin
        common_globals['BaseYealinkPgAssociator'] = BaseYealinkPgAssociator

    return module_initializer('entry', {'execfile_': execfile_})


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

    @patch('v86.common.FetchfwPluginHelper')
    @patch('v86.common.TemplatePluginHelper')
    def test_common_configure(self, template_plugin_helper, fetch_fw, v86_entry):
        plugin = v86_entry.YealinkPlugin(MagicMock(), 'test_dir', MagicMock(), MagicMock())
        raw_config = {}
        plugin._tpl_helper.get_template.return_value = 'template'
        plugin.configure_common(raw_config)
        template_plugin_helper.assert_called_once()
        plugin._tpl_helper.get_template.assert_called_with('common/dect_model.tpl')
        assert len(plugin._tpl_helper.dump.mock_calls) == 14

    @patch('v86.common.FetchfwPluginHelper')
    @patch('v86.common.TemplatePluginHelper')
    def test_configure(self, template_plugin_helper, fetch_fw, v86_entry):
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
            'sip_lines': {},
        }
        plugin = v86_entry.YealinkPlugin(MagicMock(), 'test_dir', MagicMock(), MagicMock())
        plugin._tpl_helper.get_dev_template.return_value = 'template'
        plugin.configure(device, raw_config)
        assert raw_config['XX_country'] == 'United States'
        assert raw_config['XX_lang'] == 'English'
        assert raw_config['XX_handset_lang'] == '0'
        plugin._tpl_helper.get_dev_template.assert_called_with('805ec0d57d72.cfg', device)
        plugin._tpl_helper.dump.assert_called_with(
            'template', raw_config, 'test_dir/var/tftpboot/805ec0d57d72.cfg', 'UTF-8'
        )

    @patch('v86.common.FetchfwPluginHelper')
    def test_sensitive_file(self, fetch_fw, v86_entry):
        plugin = v86_entry.YealinkPlugin(MagicMock(), 'test_dir', MagicMock(), MagicMock())
        assert plugin.is_sensitive_filename('patate') is False
        assert plugin.is_sensitive_filename('805ec0d57d72.cfg') is True
