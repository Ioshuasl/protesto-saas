from email import policy
from email.parser import BytesParser

from fastapi import HTTPException, status

from packages.v1.ged.schemas.ged_schema import (
    GEDMultipartPayloadSchema,
    GEDSaveMultipartRequestSchema,
)


class GEDSaveMultipartPayloadAction:
    @staticmethod
    async def _parse_from_form(
        data: GEDSaveMultipartRequestSchema,
    ) -> GEDMultipartPayloadSchema:
        form = await data.request.form()
        file_data = form.get("file")
        base64_form = form.get("base64")
        file_bytes = None
        file_content_type = None
        if file_data is not None and hasattr(file_data, "read"):
            file_bytes = await file_data.read()
            file_content_type = getattr(file_data, "content_type", None)

        return GEDMultipartPayloadSchema(
            file_bytes=file_bytes,
            base64_value=str(base64_form) if base64_form else None,
            file_content_type=file_content_type,
        )

    @staticmethod
    async def _parse_from_raw_body(
        data: GEDSaveMultipartRequestSchema,
    ) -> GEDMultipartPayloadSchema:
        content_type = data.request.headers.get("content-type") or ""
        body = await data.request.body()
        raw = (
            f"Content-Type: {content_type}\r\nMIME-Version: 1.0\r\n\r\n".encode("utf-8")
            + body
        )
        message = BytesParser(policy=policy.default).parsebytes(raw)

        file_bytes = None
        base64_form = None
        file_content_type = None

        if message.is_multipart():
            for part in message.iter_parts():
                if part.get_param("name", header="content-disposition") == "file":
                    file_bytes = part.get_payload(decode=True)
                    file_content_type = part.get_content_type()
                if part.get_param("name", header="content-disposition") == "base64":
                    base64_form = part.get_content()

        return GEDMultipartPayloadSchema(
            file_bytes=file_bytes,
            base64_value=base64_form,
            file_content_type=file_content_type,
        )

    @staticmethod
    async def execute(data: GEDSaveMultipartRequestSchema) -> GEDMultipartPayloadSchema:
        request = data.request
        if hasattr(request, "headers") and hasattr(request, "body"):
            payload = await GEDSaveMultipartPayloadAction._parse_from_raw_body(data)
        else:
            payload = await GEDSaveMultipartPayloadAction._parse_from_form(data)

        has_file = bool(payload.file_bytes)
        has_base64 = isinstance(payload.base64_value, str) and bool(
            payload.base64_value.strip()
        )
        if not has_file and not has_base64:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Informe 'file' ou 'base64' no multipart/form-data.",
            )

        return payload
