from fastapi import HTTPException, status
from packages.v1.servicos.atos.actions.t_ato.t_ato_ato_anterior_action import (
    TAtoAtoAnteriorAction,
)
from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoIdSchema


class TAtoAtoAnteriorService:
    def execute(self, t_ato_id_schema: TAtoIdSchema):
        data = TAtoAtoAnteriorAction().execute(t_ato_id_schema)
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao encontramos ato anterior para o ato informado.",
            )
        return data
