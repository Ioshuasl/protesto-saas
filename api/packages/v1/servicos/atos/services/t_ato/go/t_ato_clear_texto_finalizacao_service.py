from fastapi import HTTPException, status

from packages.v1.servicos.atos.actions.t_ato.t_ato_clear_texto_finalizacao_action import (
    TAtoClearTextoFinalizacaoAction,
)
from packages.v1.servicos.atos.schemas.t_ato_schema import (
    TAtoClearTextoFinalizacaoSchema,
    TAtoIdSchema,
)
from packages.v1.servicos.atos.services.t_ato.go.t_ato_show_service import TAtoShowService


class TAtoClearTextoFinalizacaoService:
    def execute(self, data: TAtoClearTextoFinalizacaoSchema):
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

        if data.tipo_finalizacao == 1:
            data.coluna = "texto_finalizacao"

        if data.tipo_finalizacao == 2:
            data.coluna = "texto_finalizacao_traslado"

        return TAtoClearTextoFinalizacaoAction().execute(data)
