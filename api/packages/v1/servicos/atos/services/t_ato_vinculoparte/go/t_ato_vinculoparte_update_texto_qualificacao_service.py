from fastapi import HTTPException, status

from packages.v1.servicos.atos.actions.t_ato_vinculoparte.t_ato_vinculoparte_update_texto_qualificacao_action import (
    TAtoVinculoParteUpdateTextoQualificacaoAction,
)
from packages.v1.servicos.atos.schemas.t_ato_vinculoparte_schema import (
    TAtoVinculoParteTextoQualificacaoUpdateSchema,
)


class TAtoVinculoParteUpdateTextoQualificacaoService:
    """
    Serviço para atualização do TEXTO_QUALIFICACAO em T_ATO_VINCULOPARTE.
    """

    def execute(self, data: TAtoVinculoParteTextoQualificacaoUpdateSchema):
        response = TAtoVinculoParteUpdateTextoQualificacaoAction().execute(data)

        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível atualizar o TEXTO_QUALIFICACAO do vínculo de parte.",
            )

        return response
