from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_tb_regimebens_schema import GTbRegimebensIdSchema
from fastapi import HTTPException, status


class DeleteRepository(BaseRepository):

    def execute(self, regimebens_schema: GTbRegimebensIdSchema):

        try:
            # Montagem do sql
            sql = """ DELETE FROM G_TB_REGIMEBENS 
                      WHERE TB_REGIMEBENS_ID = :tb_regimebens_id 
                      RETURNING TB_REGIMEBENS_ID"""

            # Preenchimento de parâmetros
            params = {
                "tb_regimebens_id": regimebens_schema.tb_regimebens_id
            }

            # Execução do sql
            response = self.run_and_return(sql, params)

            # Retorna o resultado
            return response
    
        except Exception as e:
            # Informa que houve uma falha na exclusão
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir G_TB_REGIMEBENS: {e}"
            )