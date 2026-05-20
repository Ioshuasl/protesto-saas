from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_tb_profissao_schema import GTbProfissaoIdSchema
from fastapi import HTTPException, status


class DeleteRepository(BaseRepository):

    def execute(self, profissao_schema: GTbProfissaoIdSchema):

        try:
            # Montagem do sql
            sql = """ DELETE FROM G_TB_PROFISSAO 
                      WHERE TB_PROFISSAO_ID = :tb_profissao_id 
                      RETURNING TB_PROFISSAO_ID
                    """

            # Preenchimento de parâmetros
            params = {
                "tb_profissao_id": profissao_schema.tb_profissao_id
            }

            # Execução do sql
            response = self.run_and_return(sql, params)

            # Retorna o resultado
            return response
    
        except Exception as e:
            # Informa que houve uma falha na exclusão
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir G_TB_PROFISSAO: {e}"
            )