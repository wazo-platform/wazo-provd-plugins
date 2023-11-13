# Copyright 2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later
from unittest.mock import sentinel

from ..common import BaseFanvilPlugin


class TestPlugin:
    def test_split(self):
        fkeys = [
            ('1', sentinel.first_key),
            ('2', sentinel.second_key),
            ('3', sentinel.third_key),
            ('4', sentinel.fourth_key),
            ('7', sentinel.seventh_key),
        ]
        results_top, results_bottom = BaseFanvilPlugin._split_fkeys(fkeys, 3)
        assert results_top[1] == sentinel.first_key
        assert results_top[2] == sentinel.second_key
        assert results_top[3] == sentinel.third_key
        assert results_bottom[1] == sentinel.fourth_key
        assert results_bottom[4] == sentinel.seventh_key

    def test_paginate(self):
        fkeys = [
            {'id': 1, 'value': sentinel.first_key},
            {'id': 2, 'value': sentinel.second_key},
            {'id': 3, 'value': sentinel.third_key},
            {'id': 4, 'value': sentinel.fourth_key},
            {'id': 7, 'value': sentinel.seventh_key},
        ]
        max_page, results = BaseFanvilPlugin._paginate(fkeys, 7, 3)
        assert max_page == 3
        assert results[0] == (1, 1, fkeys[0])
        assert results[1] == (1, 2, fkeys[1])
        assert results[2] == (1, 3, fkeys[2])
        assert results[3] == (2, 1, fkeys[3])
        assert results[4] == (3, 1, fkeys[4])
