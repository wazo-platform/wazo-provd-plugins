# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypedDict
    from ..common.common import BaseHtekPlugin, BaseHtekPgAssociator  # noqa: F401

    class CommonGlobalsDict(TypedDict):
        BaseHtekPlugin: type[BaseHtekPlugin]
        BaseHtekPgAssociator: type[BaseHtekPgAssociator]


common_globals: CommonGlobalsDict = {}  # type: ignore[typeddict-item]
execfile_('common.py', common_globals)  # type: ignore[name-defined]

MODEL_VERSIONS = {
    'UC926': '2.0.4.4.58',
    'UC926E': '2.0.4.4.58',
    'UC924': '2.0.4.4.58',
    'UC924E': '2.0.4.4.58',
    'UC923': '2.0.4.4.58',
    'UC912': '2.0.4.4.58',
    'UC912E': '2.0.4.4.58',
    'UC912G': '2.0.4.4.58',
    'UC903': '2.0.4.4.58',
    'UC902': '2.0.4.4.58',
    'UC862': '2.0.4.4.58',
    'UC860': '2.0.4.4.58',
    'UC860P': '2.0.4.4.58',
    'UC842': '2.0.4.4.58',
    'UC840': '2.0.4.4.58',
    'UC840P': '2.0.4.4.58',
    'UC806': '2.0.4.4.58',
    'UC806T': '2.0.4.4.58',
    'UC804': '2.0.4.4.58',
    'UC804T': '2.0.4.4.58',
    'UC803': '2.0.4.4.58',
    'UC803T': '2.0.4.4.58',
    'UC802': '2.0.4.4.58',
    'UC802T': '2.0.4.4.58',
}

COMMON_FILES = [
    ('cfg0000.xml', 'model.tpl'),  # UC862
    ('cfg0001.xml', 'model.tpl'),  # UC842
    ('cfg0002.xml', 'model.tpl'),  # UC860
    ('cfg0003.xml', 'model.tpl'),  # UC840
    ('cfg0004.xml', 'model.tpl'),  # UC806
    ('cfg0041.xml', 'model.tpl'),  # UC806T
    ('cfg0042.xml', 'model.tpl'),  # UC806G
    ('cfg0005.xml', 'model.tpl'),  # UC804
    ('cfg0051.xml', 'model.tpl'),  # UC804T
    ('cfg0052.xml', 'model.tpl'),  # UC804G
    ('cfg0006.xml', 'model.tpl'),  # UC803 / UC803T
    ('cfg0007.xml', 'model.tpl'),  # UC802 / UC802T
    ('cfg0010.xml', 'model.tpl'),  # UC926
    ('cfg0110.xml', 'model.tpl'),  # UC926E
    ('cfg0012.xml', 'model.tpl'),  # UC924
    ('cfg0112.xml', 'model.tpl'),  # UC924E
    ('cfg0013.xml', 'model.tpl'),  # UC923
    ('cfg0016.xml', 'model.tpl'),  # UC903
    ('cfg0017.xml', 'model.tpl'),  # UC902
    ('cfg0019.xml', 'model.tpl'),  # UC912 / UC912G / UC912E
]


class HtekPlugin(common_globals['BaseHtekPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True

    pg_associator = common_globals['BaseHtekPgAssociator'](MODEL_VERSIONS)

    # Htek plugin specific stuff

    _COMMON_FILES = COMMON_FILES
