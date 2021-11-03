# -*- coding: utf-8 -*-

# Copyright 2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import
import six
import unittest

from hamcrest import (
    assert_that,
    equal_to,
    has_entries,
)
from mock import MagicMock
from provd.devices.pgasso import (
    COMPLETE_SUPPORT,
    FULL_SUPPORT,
    IMPROBABLE_SUPPORT,
    PROBABLE_SUPPORT,
)
from ..common import BaseYealinkHTTPDeviceInfoExtractor, BaseYealinkPgAssociator
from ..models import MODEL_VERSIONS


class TestCommon(unittest.TestCase):
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
        http_info_extractor = BaseYealinkHTTPDeviceInfoExtractor()
        for ua, info in ua_infos.items():
            assert_that(
                http_info_extractor._do_extract(self._mock_request(ua=ua)),
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

        http_info_extractor = BaseYealinkHTTPDeviceInfoExtractor()

        for path, mac in six.iteritems(macs_from_paths):
            assert_that(
                http_info_extractor._do_extract(self._mock_request(path=path)),
                has_entries({u'vendor': u'Yealink', u'mac': mac})
            )

    def test_plugin_association_when_all_info_match(self):
        plugin_associator = BaseYealinkPgAssociator(MODEL_VERSIONS)
        for model, version in six.iteritems(MODEL_VERSIONS):
            assert_that(
                plugin_associator._do_associate('Yealink', model, version),
                equal_to(FULL_SUPPORT),
            )

    def test_plugin_association_when_only_vendor_and_model_match(self):
        plugin_associator = BaseYealinkPgAssociator(MODEL_VERSIONS)
        for model in six.iterkeys(MODEL_VERSIONS):
            assert_that(
                plugin_associator._do_associate('Yealink', model, None),
                equal_to(COMPLETE_SUPPORT),
            )

    def test_plugin_association_when_only_vendor_matches(self):
        plugin_associator = BaseYealinkPgAssociator(MODEL_VERSIONS)
        assert_that(
            plugin_associator._do_associate('Yealink', None, None),
            equal_to(PROBABLE_SUPPORT),
        )

    def test_plugin_association_when_nothing_matches(self):
        plugin_associator = BaseYealinkPgAssociator(MODEL_VERSIONS)
        assert_that(
            plugin_associator._do_associate('DoesNotMatch', 'NothingPhone', '1.2.3'),
            equal_to(IMPROBABLE_SUPPORT),
        )

    def test_plugin_association_does_not_match_when_empty_strings(self):
        plugin_associator = BaseYealinkPgAssociator(MODEL_VERSIONS)
        assert_that(
            plugin_associator._do_associate('', '', ''),
            equal_to(IMPROBABLE_SUPPORT),
        )
