from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.servicos.atos.schemas.t_ato_vinculoparte_schema import (
    TAtoVinculoParteIdSchema,
)


class TAtoVinculoParteShowTextoQualificacaoRepository(BaseRepository):
    """
    Repositório responsável pela leitura do TEXTO_QUALIFICACAO de um vínculo de parte.
    """

    def execute(self, data: TAtoVinculoParteIdSchema):
        try:
            sql = """
                SELECT
                    ATO_VINCULOPARTE_ID,
                    MARCACAO_TIPO_ID,
                    TEXTO_QUALIFICACAO
                FROM T_ATO_VINCULOPARTE
                WHERE ATO_VINCULOPARTE_ID = :ato_vinculoparte_id
            """
            params = data.model_dump(exclude_unset=True)
            result = self.fetch_one(sql, params)

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Registro de T_ATO_VINCULOPARTE não encontrado.",
                )

            return result
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao buscar TEXTO_QUALIFICACAO em T_ATO_VINCULOPARTE: {e}",
            )
