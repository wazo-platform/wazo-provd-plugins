import pytest
from unittest.mock import MagicMock, patch

from ..common import BaseYealinkPgAssociator, BaseYealinkPlugin


@pytest.fixture
def v83_entry(module_initializer):
    def execfile_(_, common_globals):
        common_globals['BaseYealinkPlugin'] = BaseYealinkPlugin
        common_globals['BaseYealinkPgAssociator'] = BaseYealinkPgAssociator

    return module_initializer('entry', {'execfile_': execfile_})


@pytest.fixture
def v83_plugin(v83_entry):
    with patch('plugins.wazo_yealink.v83.common.FetchfwPluginHelper'), patch(
        'plugins.wazo_yealink.v83.common.TemplatePluginHelper'
    ):
        yield v83_entry.YealinkPlugin(MagicMock(), 'test_dir', MagicMock(), MagicMock())
