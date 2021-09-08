# -*- coding: utf-8 -*-

# Copyright 2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from hamcrest import (
    assert_that,
    has_entries,
)
from mock import MagicMock, patch

from ..common import BaseYealinkHTTPDeviceInfoExtractor


class TestCommon(unittest.TestCase):
    def _mock_request(self, ua=None):
        request = MagicMock()
        request.getHeader = MagicMock(return_value=ua)
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

    def test_plugin_association_when_valid(self):
        pass

    def test_plugin_association_when_invalid(self):
        pass
