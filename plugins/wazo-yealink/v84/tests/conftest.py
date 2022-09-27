import pytest
from mock import MagicMock, patch

from ..common import BaseYealinkPgAssociator, BaseYealinkPlugin


@pytest.fixture
def v84_entry(module_initializer):
    def execfile_(_, common_globals):
        common_globals['BaseYealinkPlugin'] = BaseYealinkPlugin
        common_globals['BaseYealinkPgAssociator'] = BaseYealinkPgAssociator

    return module_initializer('entry', {'execfile_': execfile_})


@pytest.fixture
def v84_plugin(v84_entry):
    with patch('v84.common.FetchfwPluginHelper'), patch('v84.common.TemplatePluginHelper'):
        yield v84_entry.YealinkPlugin(MagicMock(), 'test_dir', MagicMock(), MagicMock())
