from fastapi import HTTPException, status

from packages.v1.servicos.atos.actions.t_ato.t_ato_anterior_clear_action import (
    TAtoAnteriorClearAction,
)
from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoAnteriorClearSchema


class TAtoAnteriorClearService:
    def execute(self, data: TAtoAnteriorClearSchema):
        response = TAtoAnteriorClearAction().execute(data)
        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao encontramos o ato informado para limpar dados do ato anterior.",
            )
        return response
