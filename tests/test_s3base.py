import os
import pytest
from utils.s3base import S3Base, S3ActionError

def test_get_env_var_returns_value(monkeypatch):
    monkeypatch.setenv('TEST_ENV_VAR', 'test_value')
    assert S3Base.get_env_var('TEST_ENV_VAR') == 'test_value'

def test_get_env_var_returns_default(monkeypatch):
    monkeypatch.delenv('TEST_ENV_VAR', raising=False)
    assert S3Base.get_env_var('TEST_ENV_VAR', default='default_val') == 'default_val'

def test_get_env_var_required_raises(monkeypatch):
    monkeypatch.delenv('TEST_ENV_VAR', raising=False)
    with pytest.raises(S3ActionError):
        S3Base.get_env_var('TEST_ENV_VAR', required=True)
