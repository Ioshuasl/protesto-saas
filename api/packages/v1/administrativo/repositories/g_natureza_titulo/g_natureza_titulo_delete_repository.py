from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.g_natureza_titulo_schema import (
    GNaturezaTituloIdSchema,
)


class GNaturezaTituloDeleteRepository(BaseRepository):

    def execute(self, g_natureza_titulo_id_schema: GNaturezaTituloIdSchema):

        try:
            # Montagem do SQL
            sql = """
                DELETE FROM G_NATUREZA_TITULO GNT
                WHERE GNT.NATUREZA_TITULO_ID = :natureza_titulo_id
                RETURNING GNT.NATUREZA_TITULO_ID
            """

            # Preenchimento dos parâmetros
            params = {
                "natureza_titulo_id": g_natureza_titulo_id_schema.natureza_titulo_id
            }

            # Execução da instrução SQL
            response = self.run_and_return(sql, params)

            # Retorna o resultado da exclusão
            return response

        except Exception as e:
            # Lança exceção HTTP em caso de erro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir registro de G_NATUREZA_TITULO: {e}",
            )
