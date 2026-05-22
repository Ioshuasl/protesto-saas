from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_titulo.p_titulo_show_action import ShowAction
from packages.v1.administrativo.actions.p_titulo.p_titulo_update_action import (
    UpdateAction,
)
from packages.v1.administrativo.schemas.p_titulo_schema import (
    PTituloIdSchema,
    PTituloUpdateSchema,
)


class UpdateService:
    def _ensure_exists(self, titulo_id: int):
        row = ShowAction().execute(PTituloIdSchema(titulo_id=titulo_id))
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Título não encontrado.",
            )

    def execute(self, titulo_id: int, titulo_schema: PTituloUpdateSchema):
        self._ensure_exists(titulo_id)
        return UpdateAction().execute(titulo_id, titulo_schema)
