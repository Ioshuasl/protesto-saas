from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_titulo.p_titulo_show_action import ShowAction
from packages.v1.administrativo.schemas.p_titulo_schema import PTituloIdSchema


class ShowService:
    def execute(self, titulo_schema: PTituloIdSchema):
        row = ShowAction().execute(titulo_schema)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Título não encontrado.",
            )
        return row
