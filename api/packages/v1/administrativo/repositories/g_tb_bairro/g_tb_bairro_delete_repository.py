from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_tb_bairro_schema import GTbBairroIdSchema
from fastapi import HTTPException, status


class DeleteRepository(BaseRepository):

    def execute(self, bairro_schema: GTbBairroIdSchema):

        try:
            # Montagem do sql
            sql = """ DELETE FROM G_TB_BAIRRO 
                      WHERE TB_BAIRRO_ID = :tb_bairro_id 
                      RETURNING TB_BAIRRO_ID
                    """

            # Preenchimento de parâmetros
            params = {
                "tb_bairro_id": bairro_schema.tb_bairro_id
            }

            # Execução do sql
            response = self.run_and_return(sql, params)

            # Retorna o resultado
            return response
    
        except Exception as e:
            # Informa que houve uma falha na exclusão
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir G_TB_BAIRRO: {e}"
            )