import pytest

from database import orm_firebird_settings as settings


@pytest.mark.unit
def test_use_orm_firebird_parses_true(monkeypatch):
    settings.use_orm_firebird.cache_clear()

    class FakeEnv:
        USE_ORM_FIREBIRD = "true"

    monkeypatch.setattr(settings, "EnvConfigLoader", lambda _path: FakeEnv())
    assert settings.use_orm_firebird() is True
    settings.use_orm_firebird.cache_clear()


@pytest.mark.unit
def test_use_orm_firebird_parses_false(monkeypatch):
    settings.use_orm_firebird.cache_clear()

    class FakeEnv:
        USE_ORM_FIREBIRD = "false"

    monkeypatch.setattr(settings, "EnvConfigLoader", lambda _path: FakeEnv())
    assert settings.use_orm_firebird() is False
    settings.use_orm_firebird.cache_clear()
