from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_titulo.p_titulo_selos_action import SelosAction
from packages.v1.administrativo.repositories.p_titulo.p_titulo_selos_repository import (
    SelosRepository,
)
from packages.v1.administrativo.schemas.p_titulo_schema import PTituloIdSchema


class SelosService:
    def execute(self, titulo_schema: PTituloIdSchema) -> list[dict]:
        if not SelosRepository().titulo_exists(titulo_schema.titulo_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Título não encontrado.",
            )
        return SelosAction().execute(titulo_schema)
