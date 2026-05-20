from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.g_gramatica_schema import GGramaticaIdSchema


class GGramaticaDeleteRepository(BaseRepository):

    def execute(self, g_gramatica_id_schema: GGramaticaIdSchema):

        try:
            # Montagem do SQL
            sql = """
                DELETE FROM G_GRAMATICA GG
                WHERE GG.GRAMATICA_ID = :gramatica_id
                RETURNING GG.GRAMATICA_ID
            """

            # Preenchimento dos parâmetros
            params = {"gramatica_id": g_gramatica_id_schema.gramatica_id}

            # Execução da instrução SQL
            response = self.run_and_return(sql, params)

            # Retorna o resultado da exclusão
            return response

        except Exception as e:
            # Lança exceção HTTP em caso de erro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir registro de G_GRAMATICA: {e}",
            )
