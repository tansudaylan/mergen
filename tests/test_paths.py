import os

import mergen


def test_mergen_pathbase_uses_env_var(monkeypatch):
    monkeypatch.setenv('MERGEN_DATA_PATH', '/tmp/mergen-data')
    expected = os.path.abspath('/tmp/mergen-data') + os.sep
    assert mergen.util.retr_pathbase() == expected


def test_catalog_utils_defaults_are_not_machine_specific(monkeypatch):
    monkeypatch.setenv('MERGEN_DATA_PATH', '/tmp/mergen-data')
    assert mergen.catalog_utils.query_vizier.__defaults__[-2] is None
    assert mergen.catalog_utils.get_otype_dict.__defaults__ == (None,)
