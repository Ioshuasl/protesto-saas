from __future__ import annotations

import logging

from fastapi import HTTPException, status

from actions.data.rtf_blob_codec import RTFBlobCodec
from actions.env.env_config_loader import EnvConfigLoader
from packages.v1.administrativo.actions.p_template.p_template_update_texto_action import (
    UpdateTextoAction,
)
from packages.v1.administrativo.schemas.p_template_schema import (
    PTemplateEditorCallbackSchema,
    PTemplateUpdateTextoSchema,
)
from packages.v1.docx.actions.docx_load_only_office_file_bytes_action import (
    DOCXLoadOnlyOfficeFileBytesAction,
)
from packages.v1.docx.services.docx_rtf_convert_service import DocxRtfConvertService
from packages.v1.docx.services.docx_wptools_marker_highlight_service import (
    strip_marker_highlights_from_docx_bytes,
)
from packages.v1.docx.schemas.docx_schema import DOCXSchemaCallback

logger = logging.getLogger(__name__)


class SaveEditorCallbackService:
    SAVE_STATUSES = {2, 6}

    def execute(self, data: PTemplateEditorCallbackSchema):
        self._validate_callback_token(data.callback_token)

        status_value = int(data.data.get("status") or 0)
        callback_file_url = data.data.get("url")
        logger.info(
            "OnlyOffice callback recebido para p_template",
            extra={
                "template_id": data.template_id,
                "status": status_value,
                "url": callback_file_url,
            },
        )
        if status_value not in self.SAVE_STATUSES:
            return {"saved": False, "status": status_value}

        onlyoffice_callback = DOCXSchemaCallback(
            registro_id=data.template_id,
            servico="p_template_update_texto_service",
            data=data.data,
        )
        file_bytes = DOCXLoadOnlyOfficeFileBytesAction.execute(onlyoffice_callback)
        file_bytes = strip_marker_highlights_from_docx_bytes(file_bytes)
        rtf_text = DocxRtfConvertService.docx_bytes_to_rtf_text(file_bytes)
        compressed_blob = RTFBlobCodec.rtf_text_to_blob(rtf_text)

        updated = UpdateTextoAction().execute(
            PTemplateUpdateTextoSchema(
                template_id=data.template_id,
                texto=compressed_blob,
            )
        )
        logger.info(
            "OnlyOffice callback salvo com sucesso para p_template",
            extra={
                "template_id": data.template_id,
                "status": status_value,
                "url": callback_file_url,
            },
        )
        return {"saved": True, "status": status_value, "data": updated}

    @staticmethod
    def _validate_callback_token(incoming_token: str | None) -> None:
        env = EnvConfigLoader(".env")
        expected = getattr(env, "ORIUS_EDITOR_CALLBACK_TOKEN", None)
        if not expected:
            return

        if incoming_token != expected:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Callback token inválido.",
            )

