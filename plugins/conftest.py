from __future__ import annotations

import importlib.util
from collections.abc import Generator
from os.path import basename
from types import ModuleType
from typing import Any, Callable

import pytest
from pytest import FixtureRequest

ModuleInitializer = Callable[[str, dict[str, Any]], ModuleType]


@pytest.fixture()
def module_initializer(
    request: FixtureRequest,
) -> Generator[ModuleInitializer, None, None]:
    """
    Create a method to import files that need global overrides or special
    modifications before import.
    This is usually just the entry.py, but could be used with others.
    The fixture will automatically use the path of the module using it.
    """
    plugin_base_path = request.path.parents[2]
    plugin_version = basename(request.path.parents[1])

    def initialize_module(module_name: str, global_overrides: dict[str, Any]):
        module_file_path = plugin_base_path / plugin_version / f'{module_name}.py'
        spec = importlib.util.spec_from_file_location(
            f'{plugin_version}.{module_name}',
            module_file_path,
            submodule_search_locations=[str(plugin_base_path / plugin_version)],
        )
        module = importlib.util.module_from_spec(spec)
        if global_overrides is not None:
            module.__dict__.update(global_overrides)
        spec.loader.exec_module(module)
        return module

    yield initialize_module
