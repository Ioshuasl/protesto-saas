from fastapi import HTTPException, status

from packages.v1.servicos.atos.actions.t_ato.t_ato_anterior_update_action import (
    TAtoAnteriorUpdateAction,
)
from packages.v1.servicos.atos.actions.t_ato.t_ato_show_action import TAtoShowAction
from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoAnteriorUpdateSchema, TAtoIdSchema


class TAtoAnteriorUpdateService:
    def execute(self, data: TAtoAnteriorUpdateSchema):

        response_ato_show = TAtoShowAction().execute(TAtoIdSchema(ato_id=data.ato_id))
        if not response_ato_show:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi localizado o registro pai",
            )

        response_ato_anterior_update = TAtoAnteriorUpdateAction().execute(data)
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao encontramos o ato informado para atualizacao.",
            )
        return response_ato_anterior_update
