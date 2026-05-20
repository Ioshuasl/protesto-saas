from packages.v1.administrativo.schemas.g_tb_regimecomunhao_schema import \
    GTbRegimecomunhaoIdSchema
from abstracts.repository import BaseRepository
from fastapi import HTTPException, status


class DeleteRepository(BaseRepository):

    def execute(self, regimecomunhao_schema: GTbRegimecomunhaoIdSchema):

        try:

            # Montagem do sql
            sql = """ DELETE FROM G_TB_REGIMECOMUNHAO GTB 
                      WHERE GTB.tb_regimecomunhao_id = :tb_regimecomunhao_id 
                      RETURNING GTB.tb_regimecomunhao_id
                """

            # Preenchimento de parâmetros
            params = {
                "tb_regimecomunhao_id": regimecomunhao_schema.tb_regimecomunhao_id
            }

            # Execução do sql
            response = self.run_and_return(sql, params)

            # Retorna o resultado
            return response

        except Exception as e:

            # Informa que houve uma falha na atualização do usuário
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir G_TB_REGIMECOMUNHAO: {e}"
            )