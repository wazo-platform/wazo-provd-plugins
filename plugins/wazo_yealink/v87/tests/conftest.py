from unittest.mock import MagicMock, patch

import pytest

from ..common import BaseYealinkPgAssociator, BaseYealinkPlugin


@pytest.fixture
def v86_entry(module_initializer):
    def execfile_(_, common_globals):
        common_globals['BaseYealinkPlugin'] = BaseYealinkPlugin
        common_globals['BaseYealinkPgAssociator'] = BaseYealinkPgAssociator

    return module_initializer('entry', {'execfile_': execfile_})


@pytest.fixture
def v86_plugin(v86_entry):
    with patch('plugins.wazo_yealink.v86.common.FetchfwPluginHelper'), patch(
        'plugins.wazo_yealink.v86.common.TemplatePluginHelper'
    ):
        yield v86_entry.YealinkPlugin(MagicMock(), 'test_dir', MagicMock(), MagicMock())
