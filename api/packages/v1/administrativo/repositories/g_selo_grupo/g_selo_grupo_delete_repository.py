from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.g_selo_grupo_schema import GSeloGrupoIdSchema


class GSeloGrupoDeleteRepository(BaseRepository):

    def execute(self, g_selo_grupo_id_schema: GSeloGrupoIdSchema):

        try:
            # Montagem do SQL
            sql = """
                DELETE FROM G_SELO_GRUPO GSG
                WHERE GSG.SELO_GRUPO_ID = :selo_grupo_id
                RETURNING GSG.SELO_GRUPO_ID
            """

            # Preenchimento dos parâmetros
            params = {"selo_grupo_id": g_selo_grupo_id_schema.selo_grupo_id}

            # Execução da instrução SQL
            response = self.run_and_return(sql, params)

            # Retorna o resultado da exclusão
            return response

        except Exception as e:
            # Lança exceção HTTP em caso de erro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir registro de G_SELO_GRUPO: {e}",
            )
