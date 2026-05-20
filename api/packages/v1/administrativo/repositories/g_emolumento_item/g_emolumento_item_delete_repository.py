from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.g_emolumento_item_schema import GEmolumentoItemIdSchema


class GEmolumentoItemDeleteRepository(BaseRepository):

    def execute(self, g_emolumento_item_id_schema: GEmolumentoItemIdSchema):

        try:
            # Montagem do SQL
            sql = """
                DELETE FROM g_emolumento_item GG
                WHERE GG.emolumento_item_id = :emolumento_item_id
                RETURNING GG.emolumento_item_id
            """

            # Preenchimento dos parâmetros
            params = {
                "emolumento_item_id": g_emolumento_item_id_schema.emolumento_item_id
            }

            # Execução da instrução SQL
            response = self.run_and_return(sql, params)

            # Retorna o resultado da exclusão
            return response

        except Exception as e:
            # Lança exceção HTTP em caso de erro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir registro de G_EMOLUMENTO_ITEM: {e}"
            )
