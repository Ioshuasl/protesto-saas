from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.g_emolumento_schema import GEmolumentoIdSchema


class GEmolumentoDeleteRepository(BaseRepository):

    def execute(self, g_emolumento_id_schema: GEmolumentoIdSchema):

        try:
            # Montagem do SQL
            sql = """
                DELETE FROM G_EMOLUMENTO GE
                WHERE GE.EMOLUMENTO_ID = :emolumento_id
                RETURNING GE.EMOLUMENTO_ID
            """

            # Preenchimento dos parâmetros
            params = {"emolumento_id": g_emolumento_id_schema.emolumento_id}

            # Execução da instrução SQL
            response = self.run_and_return(sql, params)

            # Retorna o resultado da exclusão
            return response

        except Exception as e:
            # Lança exceção HTTP em caso de erro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir registro de G_EMOLUMENTO: {e}",
            )
