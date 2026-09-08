import importlib


def test_import_mergen_package():
    mergen = importlib.import_module('mergen')
    assert hasattr(mergen, '__file__')


def test_import_mergen_module():
    coll_tran = importlib.import_module('mergen.coll_tran')
    assert hasattr(coll_tran, 'main')
