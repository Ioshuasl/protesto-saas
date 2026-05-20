from fastapi import HTTPException, status

from packages.v1.servicos.atos.actions.t_ato.t_ato_update_texto_assinatura_action import (
    TAtoUpdateTextoAssinaturaAction,
)
from packages.v1.servicos.atos.schemas.t_ato_schema import (
    TAtoIdSchema,
    TAtoTextoAssinaturaUpdateSchema,
)
from packages.v1.servicos.atos.services.t_ato.go.t_ato_show_service import TAtoShowService


class TAtoUpdateTextoAssinaturaService:

    def execute(self, data: TAtoTextoAssinaturaUpdateSchema):

        response_ato = TAtoShowService().execute(
            TAtoIdSchema(
                ato_id=data.ato_id,
            )
        )

        if not response_ato:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao encontramos o ato informado. Verifique o codigo e tente novamente.",
            )

        return TAtoUpdateTextoAssinaturaAction().execute(data)
