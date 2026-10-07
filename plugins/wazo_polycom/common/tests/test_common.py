# Copyright 2026 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from ..common import BasePolycomHTTPDeviceInfoExtractor

UA_WITH_SN = (
    b'FileTransport PolycomVVX-VVX_500-UA/5.9.2.3446 (SN:0004f2123456) Type/Application'
)
UA_WITHOUT_SN = b'FileTransport PolycomVVX-VVX_400-UA/4.1.4.7430 Type/Application'


class TestInfoExtraction:
    http_info_extractor: BasePolycomHTTPDeviceInfoExtractor

    @classmethod
    def setup_class(cls):
        cls.http_info_extractor = BasePolycomHTTPDeviceInfoExtractor()

    def _mock_request(self, ua: bytes | None = None, path: bytes | None = None):
        request = MagicMock()
        request.getHeader = MagicMock(return_value=ua)
        request.path = path
        return request

    @pytest.mark.parametrize(
        'path',
        [
            b'/000000000000.cfg',
            b'/common.cfg',
            b'/sip.ld',
            b'/SoundPointIPLocalization/English_United_States/SoundPointIP-dictionary.xml',
        ],
    )
    def test_mac_from_ua_serial_number_when_not_in_path(self, path):
        result = self.http_info_extractor._do_extract(
            self._mock_request(ua=UA_WITH_SN, path=path)
        )

        assert result is not None
        assert {
            'vendor': 'Polycom',
            'model': 'VVX500',
            'mac': '00:04:f2:12:34:56',
        }.items() <= result.items()

    def test_mac_from_path_takes_precedence_over_ua_serial_number(self):
        result = self.http_info_extractor._do_extract(
            self._mock_request(ua=UA_WITH_SN, path=b'/0004f2abcdef-phone.cfg')
        )

        assert result == {
            'vendor': 'Polycom',
            'model': 'VVX500',
            'version': '5.9.2.3446',
            'mac': '00:04:f2:ab:cd:ef',
        }

    def test_uppercase_serial_number_is_normalized(self):
        ua = b'FileTransport PolycomVVX-VVX_500-UA/5.9.2.3446 (SN:0004F2ABCDEF) Type/Application'

        result = self.http_info_extractor._do_extract(
            self._mock_request(ua=ua, path=b'/000000000000.cfg')
        )

        assert result is not None
        assert result['mac'] == '00:04:f2:ab:cd:ef'

    def test_no_mac_when_ua_has_no_serial_number(self):
        result = self.http_info_extractor._do_extract(
            self._mock_request(ua=UA_WITHOUT_SN, path=b'/000000000000.cfg')
        )

        assert result == {'vendor': 'Polycom', 'model': 'VVX400'}

    def test_no_mac_when_serial_number_is_null(self):
        ua = b'FileTransport PolycomVVX-VVX_500-UA/5.9.2.3446 (SN:000000000000) Type/Application'

        result = self.http_info_extractor._do_extract(
            self._mock_request(ua=ua, path=b'/000000000000.cfg')
        )

        assert result is not None
        assert 'mac' not in result

    def test_no_info_when_ua_is_not_polycom(self):
        result = self.http_info_extractor._do_extract(
            self._mock_request(ua=b'Mozilla/5.0 (SN:0004f2123456)', path=b'/common.cfg')
        )

        assert result is None
