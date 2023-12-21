from unittest.mock import MagicMock, patch

import pytest

from ..common import BaseYealinkPgAssociator, BaseYealinkPlugin


@pytest.fixture
def v85_entry(module_initializer):
    def execfile_(_, common_globals):
        common_globals['BaseYealinkPlugin'] = BaseYealinkPlugin
        common_globals['BaseYealinkPgAssociator'] = BaseYealinkPgAssociator

    return module_initializer('entry', {'execfile_': execfile_})


@pytest.fixture
def v85_plugin(v85_entry):
    with patch('plugins.wazo_yealink.v85.common.FetchfwPluginHelper'), patch(
        'plugins.wazo_yealink.v85.common.TemplatePluginHelper'
    ):
        yield v85_entry.YealinkPlugin(MagicMock(), 'test_dir', MagicMock(), MagicMock())
