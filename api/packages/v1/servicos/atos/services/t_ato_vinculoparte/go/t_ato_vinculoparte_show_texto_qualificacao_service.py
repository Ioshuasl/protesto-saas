from fastapi import HTTPException, status

from packages.v1.docx.services.docx_process_service import DOCXProcess, DOCXProcessSchema
from packages.v1.servicos.atos.actions.t_ato_vinculoparte.t_ato_vinculoparte_show_texto_qualificacao_action import (
    TAtoVinculoParteShowTextoQualificacaoAction,
)
from packages.v1.servicos.atos.schemas.t_ato_vinculoparte_schema import (
    TAtoVinculoParteIdSchema,
)


class TAtoVinculoParteShowTextoQualificacaoService:
    """
    Serviço para leitura do TEXTO_QUALIFICACAO em T_ATO_VINCULOPARTE.
    """

    def execute(self, data: TAtoVinculoParteIdSchema):
        response = TAtoVinculoParteShowTextoQualificacaoAction().execute(data)

        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o TEXTO_QUALIFICACAO do vínculo de parte.",
            )

        response.texto_qualificacao = DOCXProcess().execute(
            DOCXProcessSchema(
                id=f"{response.ato_vinculoparte_id}_texto_qualificacao",
                content=response.texto_qualificacao,
                output="path",
            )
        )

        print(response.texto_qualificacao)

        return response
