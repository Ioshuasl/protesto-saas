from unittest.mock import patch

import pytest

from packages.v1.docx.services.docx_rtf_convert_service import DocxRtfConvertService


@pytest.mark.unit
def test_docx_bytes_to_rtf_text_normalizes_libreoffice_output():
    libreoffice_rtf = b"{\\rtf1 T\\u237\\'edtulo}"

    with patch(
        "packages.v1.docx.services.docx_rtf_convert_service.SofficeConvertAction.convert_bytes",
        return_value=libreoffice_rtf,
    ):
        result = DocxRtfConvertService.docx_bytes_to_rtf_text(b"PK\x03\x04fake")

    assert "\\'ed" not in result.lower() or "\\u237?" in result
    assert "íí" not in result
