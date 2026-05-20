from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.g_cartorio_schema import GCartorioIdSchema


class GCartorioDeleteRepository(BaseRepository):

    def execute(self, g_cartorio_id_schema: GCartorioIdSchema):

        try:
            # Montagem do SQL
            sql = """
                DELETE FROM G_CARTORIO GC
                WHERE GC.CARTORIO_ID = :cartorio_id
                RETURNING GC.CARTORIO_ID
            """

            # Preenchimento dos parâmetros
            params = {"cartorio_id": g_cartorio_id_schema.cartorio_id}

            # Execução da instrução SQL
            response = self.run_and_return(sql, params)

            # Retorna o resultado da exclusão
            return response

        except Exception as e:
            # Lança exceção HTTP em caso de erro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir registro de G_CARTORIO: {e}",
            )
