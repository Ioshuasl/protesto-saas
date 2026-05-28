from __future__ import annotations

import time
from urllib.parse import urlencode

from fastapi import Request

from actions.data.rtf_blob_codec import RTFBlobCodec
from actions.env.env_config_loader import EnvConfigLoader
from packages.v1.administrativo.actions.p_template.p_template_show_texto_action import (
    ShowTextoAction,
)
from packages.v1.administrativo.schemas.p_template_schema import (
    PTemplateEditorOpenSchema,
    PTemplateIdSchema,
)
from packages.v1.docx.services.docx_process_service import DOCXProcess, DOCXProcessSchema


class OpenEditorService:
    def execute(
        self,
        template_id: int,
        request: Request,
        editor_schema: PTemplateEditorOpenSchema,
    ) -> dict:
        row = ShowTextoAction().execute(PTemplateIdSchema(template_id=template_id))
        rtf_text = RTFBlobCodec.blob_to_rtf_text(row.get("texto"))

        filename = DOCXProcess().execute(
            DOCXProcessSchema(
                id=f"p_template_{template_id}",
                content=rtf_text,
                output="path",
                save_disk=True,
                storage_dir="./storage/temp",
                filename_prefix=f"p_template_{template_id}",
            )
        )

        file_url = self._build_temp_url(request, filename)
        callback_url = self._build_callback_url(request, template_id)

        key = f"p_template_{template_id}_{int(time.time())}"
        title = f"template_{template_id}.docx"
        descricao = row.get("descricao") or ""

        env = EnvConfigLoader(".env")
        editor_url = getattr(env, "ORIUS_EDITOR", None)

        return {
            "template_id": template_id,
            "descricao": descricao,
            "document_server_url": editor_url,
            "document": {
                "fileType": "docx",
                "key": key,
                "title": title,
                "url": file_url,
            },
            "editorConfig": {
                "callbackUrl": callback_url,
                "mode": editor_schema.mode,
                "lang": "pt-BR",
            },
        }

    @staticmethod
    def _build_temp_url(request: Request, filename: str) -> str:
        base = str(request.base_url).rstrip("/")
        return f"{base}/temp/{filename}"

    @staticmethod
    def _build_callback_url(request: Request, template_id: int) -> str:
        callback_url = str(
            request.url_for("p_template_texto_callback", template_id=template_id)
        )
        env = EnvConfigLoader(".env")
        callback_token = getattr(env, "ORIUS_EDITOR_CALLBACK_TOKEN", None)
        if callback_token:
            return f"{callback_url}?{urlencode({'token': callback_token})}"
        return callback_url

