from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_tb_reconhecimentotipo_schema import TTbReconhecimentotipoIdSchema
from fastapi import HTTPException, status

class DeleteRepository(BaseRepository):

    def execute(self, reconhecimentotipo_schema: TTbReconhecimentotipoIdSchema):

        try:
            # Montagem do sql
            sql = """ 
                    DELETE FROM T_TB_RECONHECIMENTOTIPO 
                    WHERE TB_RECONHECIMENTOTIPO_ID = :tb_reconhecimentotipo_id 
                    RETURNING TB_RECONHECIMENTOTIPO_ID
                """

            # Preenchimento de parâmetros
            params = {
                "tb_reconhecimentotipo_id": reconhecimentotipo_schema.tb_reconhecimentotipo_id
            }

            # Execução do sql
            response = self.run_and_return(sql, params)

            # Retorna o resultado
            return response
    
        except Exception as e:
            # Informa que houve uma falha na exclusão
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir T_TB_RECONHECIMENTOTIPO: {e}"
            )
