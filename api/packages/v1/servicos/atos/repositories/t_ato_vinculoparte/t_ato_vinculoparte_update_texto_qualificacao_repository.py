from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.servicos.atos.schemas.t_ato_vinculoparte_schema import (
    TAtoVinculoParteTextoQualificacaoUpdateSchema,
)


class TAtoVinculoParteUpdateTextoQualificacaoRepository(BaseRepository):
    """
    Repositório responsável pela atualização do TEXTO_QUALIFICACAO em T_ATO_VINCULOPARTE.
    """

    def execute(self, data: TAtoVinculoParteTextoQualificacaoUpdateSchema):
        try:
            params = data.model_dump(exclude_unset=True)

            sql = """
                UPDATE T_ATO_VINCULOPARTE
                   SET TEXTO_QUALIFICACAO = :texto_qualificacao
                 WHERE ATO_VINCULOPARTE_ID = :ato_vinculoparte_id
                RETURNING ATO_VINCULOPARTE_ID, MARCACAO_TIPO_ID, TEXTO_QUALIFICACAO
            """
            response = self.run_and_return(sql, params)

            if not response:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Registro de T_ATO_VINCULOPARTE não encontrado.",
                )

            return response
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar TEXTO_QUALIFICACAO em T_ATO_VINCULOPARTE: {e}",
            )
