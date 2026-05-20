from fastapi import HTTPException, status

from packages.v1.servicos.atos.actions.t_ato.t_ato_clear_texto_action import (
    TAtoClearTextoAction,
)
from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoClearTextoSchema


class TAtoClearTextoService:
    def execute(self, data: TAtoClearTextoSchema):
        response = TAtoClearTextoAction().execute(data)

        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao encontramos o ato informado. Verifique o codigo e tente novamente.",
            )

        return response
