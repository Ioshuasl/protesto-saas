import pytest


@pytest.fixture
def fake_current_user():
    return {"data": {"usuario_id": 1}}
