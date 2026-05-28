import pytest

from database.orm_firebird import is_firebird_connection_error


@pytest.mark.unit
def test_is_firebird_connection_error_detects_network_failure():
    exc = Exception(
        'Unable to complete network request to host "localhost". '
        "-Failed to establish a connection."
    )
    assert is_firebird_connection_error(exc) is True


@pytest.mark.unit
def test_is_firebird_connection_error_ignores_other_errors():
    assert is_firebird_connection_error(ValueError("campo invalido")) is False
