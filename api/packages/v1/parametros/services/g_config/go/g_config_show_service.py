import base64

from fastapi import HTTPException, status

from packages.v1.parametros.actions.g_config.g_config_show_action import GConfigShowAction
from packages.v1.parametros.schemas.g_config_schema import GConfigIdSchema
from packages.v1.docx.services.docx_process_service import (
    DOCXProcess,
    DOCXProcessSchema,
)


class GConfigShowService:
    def execute(self, data: GConfigIdSchema):
        show_action = GConfigShowAction()
        data = show_action.execute(data)
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao foi possivel localizar o registro de G_CONFIG",
            )

        content = data.texto if data.texto else b""
        data.texto = DOCXProcess().execute(
            DOCXProcessSchema(
                id=str(data.config_id),
                content=content,
                save_disk=True,
            )
        )

        return data
