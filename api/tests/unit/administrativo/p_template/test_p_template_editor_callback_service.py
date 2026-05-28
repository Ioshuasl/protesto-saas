from unittest.mock import patch

import pytest
from fastapi import HTTPException

from packages.v1.administrativo.schemas.p_template_schema import (
    PTemplateEditorCallbackSchema,
)
from packages.v1.administrativo.services.p_template.go.p_template_save_editor_callback_service import (
    SaveEditorCallbackService,
)


@pytest.mark.unit
def test_callback_service_ignores_non_save_status():
    schema = PTemplateEditorCallbackSchema(
        template_id=10,
        data={"status": 1},
        callback_token=None,
    )

    result = SaveEditorCallbackService().execute(schema)

    assert result == {"saved": False, "status": 1}


@pytest.mark.unit
def test_callback_service_updates_blob_on_status_2():
    schema = PTemplateEditorCallbackSchema(
        template_id=10,
        data={"status": 2, "url": "http://editor/cache/file.docx"},
        callback_token=None,
    )

    with patch(
        "packages.v1.administrativo.services.p_template.go.p_template_save_editor_callback_service."
        "SaveEditorCallbackService._validate_callback_token",
        return_value=None,
    ):
        with patch(
            "packages.v1.administrativo.services.p_template.go.p_template_save_editor_callback_service."
            "DOCXLoadOnlyOfficeFileBytesAction.execute",
            return_value=b"PK\x03\x04fake-docx",
        ):
            with patch(
                "packages.v1.administrativo.services.p_template.go.p_template_save_editor_callback_service."
                "DOCXConvertToRTFAction.execute",
                return_value=rb"{\rtf1\ansi teste}",
            ):
                with patch(
                    "packages.v1.administrativo.services.p_template.go.p_template_save_editor_callback_service."
                    "UpdateTextoAction.execute",
                    return_value={"template_id": 10, "descricao": "Template"},
                ) as update_mock:
                    result = SaveEditorCallbackService().execute(schema)

    assert result["saved"] is True
    assert result["status"] == 2
    assert result["data"]["template_id"] == 10
    update_mock.assert_called_once()


@pytest.mark.unit
def test_callback_service_rejects_invalid_token_when_required():
    schema = PTemplateEditorCallbackSchema(
        template_id=10,
        data={"status": 2},
        callback_token="invalid",
    )

    with patch(
        "packages.v1.administrativo.services.p_template.go.p_template_save_editor_callback_service."
        "EnvConfigLoader"
    ) as env_loader:
        env_loader.return_value.ORIUS_EDITOR_CALLBACK_TOKEN = "expected"
        with pytest.raises(HTTPException) as exc_info:
            SaveEditorCallbackService().execute(schema)

    assert exc_info.value.status_code == 401

