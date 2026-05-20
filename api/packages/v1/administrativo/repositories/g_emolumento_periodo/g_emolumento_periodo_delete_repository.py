from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.g_emolumento_periodo_schema import (
    GEmolumentoPeriodoIdSchema,
)


class GEmolumentoPeriodoDeleteRepository(BaseRepository):

    def execute(self, g_emolumento_periodo_id_schema: GEmolumentoPeriodoIdSchema):

        try:
            # Montagem do SQL
            sql = """
                DELETE FROM G_EMOLUMENTO_PERIODO GEP
                WHERE GEP.GEMOLUMENTO_PERIODO_ID = :emolumento_periodo_id
                RETURNING GEP.GEMOLUMENTO_PERIODO_ID
            """

            # Preenchimento dos parâmetros
            params = {
                "emolumento_periodo_id": g_emolumento_periodo_id_schema.emolumento_periodo_id
            }

            # Execução da instrução SQL
            response = self.run_and_return(sql, params)

            # Retorna o resultado da exclusão
            return response

        except Exception as e:
            # Lança exceção HTTP em caso de erro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir registro de G_EMOLUMENTO_PERIODO: {e}",
            )
