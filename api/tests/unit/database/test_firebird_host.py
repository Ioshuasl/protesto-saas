import pytest

from database.firebird_host import resolve_firebird_host


@pytest.mark.unit
def test_resolve_firebird_host_keeps_remote_host():
    assert resolve_firebird_host("10.0.0.50") == "10.0.0.50"


@pytest.mark.unit
def test_resolve_firebird_host_normalizes_loopback():
    assert resolve_firebird_host("127.0.0.1") == "localhost"
    assert resolve_firebird_host("localhost") == "localhost"
