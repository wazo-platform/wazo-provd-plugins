from os import path

import pytest
import six


@pytest.fixture()
def module_initializer(request):
    """
    Create a method to import files that need global overrides or special modifications before import.
    This is usually just the entry.py, but could be used with others.
    The fixture will automatically use the path of the module using it.
    """
    base_module = request.module.__name__.split('.')[0]
    file_path = request.module.__name__.replace('.', path.sep) + '.py'
    module_path = request.module.__file__.replace(file_path, base_module)

    def initialize_module(module_name, global_overrides):
        import imp
        from types import ModuleType

        module = ModuleType('{}.{}'.format(base_module, module_name))
        if global_overrides is not None:
            module.__dict__.update(global_overrides)
        source_file, filename = imp.find_module(module_name, [module_path])[:2]
        six.exec_(source_file.read(), module.__dict__)
        return module

    yield initialize_module
