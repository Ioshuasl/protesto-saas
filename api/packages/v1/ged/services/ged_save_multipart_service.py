import base64

from fastapi import HTTPException, status

from packages.v1.ged.actions.ged_allowed_upload_types_action import (
    GEDAllowedUploadTypesAction,
)
from packages.v1.ged.actions.ged_save_multipart_payload_action import (
    GEDSaveMultipartPayloadAction,
)
from packages.v1.ged.schemas.ged_schema import GEDSaveMultipartRequestSchema, GEDSaveSchema
from packages.v1.ged.services.ged_save_service import GEDSaveService


class GEDSaveMultipartService:
    async def execute(self, data: GEDSaveMultipartRequestSchema):
        payload = await GEDSaveMultipartPayloadAction.execute(data)
        encoded = None
        if payload.file_bytes:
            if not GEDAllowedUploadTypesAction.is_allowed(payload.file_content_type):
                allowed = ", ".join(GEDAllowedUploadTypesAction.list_allowed())
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=(
                        f"Tipo de arquivo nao permitido: {payload.file_content_type}. "
                        f"Permitidos: {allowed}"
                    ),
                )
            encoded = base64.b64encode(payload.file_bytes).decode("ascii")
        elif isinstance(payload.base64_value, str):
            encoded = payload.base64_value

        save_schema = GEDSaveSchema(
            serventia=int(data.path.serventia),
            pasta=str(data.path.pasta),
            registro_id=str(data.path.registro_id),
            base64=encoded,
        )
        return GEDSaveService().execute(save_schema)
