from fastapi import HTTPException, status

from packages.v1.servicos.atos.actions.t_ato.t_ato_clear_texto_assinatura_action import (
    TAtoClearTextoAssinaturaAction,
)
from packages.v1.servicos.atos.schemas.t_ato_schema import (
    TAtoClearTextoAssinaturaSchema,
    TAtoIdSchema,
)
from packages.v1.servicos.atos.services.t_ato.go.t_ato_show_service import TAtoShowService


class TAtoClearTextoAssinaturaService:
    def execute(self, data: TAtoClearTextoAssinaturaSchema):
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

        if data.tipo_assinatura == 1:
            data.coluna = "texto_assinatura"

        if data.tipo_assinatura == 2:
            data.coluna = "texto_assinatura_traslado"

        return TAtoClearTextoAssinaturaAction().execute(data)
