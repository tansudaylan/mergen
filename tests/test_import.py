import importlib
import importlib.util
from pathlib import Path


def test_import_mergen_package():
    mergen = importlib.import_module('mergen')
    assert hasattr(mergen, '__file__')


def test_import_mergen_module():
    coll_tran = importlib.import_module('mergen.coll_tran')
    assert hasattr(coll_tran, 'main')


def test_tutorial_module_is_import_safe():
    tutorial_path = Path(__file__).resolve().parents[1] / 'tutorial.py'
    spec = importlib.util.spec_from_file_location('mergen_tutorial_test', tutorial_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert hasattr(module, 'main')
