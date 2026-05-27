from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_titulo.p_titulo_devedores_action import (
    DevedoresAction,
)
from packages.v1.administrativo.repositories.p_titulo.p_titulo_devedores_repository import (
    DevedoresRepository,
)
from packages.v1.administrativo.schemas.p_titulo_schema import PTituloIdSchema


class DevedoresService:
    def execute(self, titulo_schema: PTituloIdSchema) -> list[dict]:
        if not DevedoresRepository().titulo_exists(titulo_schema.titulo_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Título não encontrado.",
            )
        return DevedoresAction().execute(titulo_schema)
