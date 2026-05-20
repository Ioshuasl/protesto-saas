from packages.v1.administrativo.schemas.g_tb_txmodelogrupo_schema import GTbTxmodelogrupoIdSchema
from abstracts.repository import BaseRepository
from fastapi import HTTPException, status


class DeleteRepository(BaseRepository):

    def execute(self, txmodelogrupo_schema: GTbTxmodelogrupoIdSchema):
        
        try:
            # Montagem do SQL para exclusão
            sql = """
                DELETE FROM G_TB_TXMODELOGRUPO
                WHERE TB_TXMODELOGRUPO_ID = :tb_txmodelogrupo_id
                RETURNING TB_TXMODELOGRUPO_ID
            """

            # Preenchimento de parâmetros
            params = {
                "tb_txmodelogrupo_id": txmodelogrupo_schema.tb_txmodelogrupo_id
            }

            # Execução do SQL
            response = self.run_and_return(sql, params)

            # Retorna o resultado
            return response

        except Exception as e:
            # Informa que houve uma falha na exclusão
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir modelo de grupo: {e}"
            )