import pytest
from unittest.mock import patch

from packages.v1.docx.actions.docx_load_only_office_file_bytes_action import (
    DOCXLoadOnlyOfficeFileBytesAction,
)


@pytest.mark.unit
def test_resolve_file_url_rewrites_cache_url_to_editor_host_when_different():
    file_url = "http://192.168.32.1:8080/cache/files/data/x/output.docx?md5=abc"
    expected = "http://192.168.1.140:8080/cache/files/data/x/output.docx?md5=abc"

    with patch(
        "packages.v1.docx.actions.docx_load_only_office_file_bytes_action.EnvConfigLoader"
    ) as env_loader:
        env_loader.return_value.ORIUS_EDITOR = "http://192.168.1.140:8080"
        resolved = DOCXLoadOnlyOfficeFileBytesAction._resolve_file_url(file_url)

    assert resolved == expected


@pytest.mark.unit
def test_resolve_file_url_protocol_relative_is_normalized_to_http():
    file_url = "//192.168.32.1:8080/cache/files/data/x/output.docx?md5=abc"
    expected = "http://192.168.1.140:8080/cache/files/data/x/output.docx?md5=abc"

    with patch(
        "packages.v1.docx.actions.docx_load_only_office_file_bytes_action.EnvConfigLoader"
    ) as env_loader:
        env_loader.return_value.ORIUS_EDITOR = "http://192.168.1.140:8080"
        resolved = DOCXLoadOnlyOfficeFileBytesAction._resolve_file_url(file_url)

    assert resolved == expected

