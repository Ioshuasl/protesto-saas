from fastapi import HTTPException, status

from packages.v1.administrativo.actions.g_feriado.g_feriado_show_action import ShowAction
from packages.v1.administrativo.schemas.g_feriado_schema import GFeriadoIdSchema


class ShowService:
    def execute(self, feriado_schema: GFeriadoIdSchema):
        show_action = ShowAction()
        data = show_action.execute(feriado_schema)

        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o feriado.",
            )

        return data
