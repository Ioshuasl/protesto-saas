from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_censec_schema import TCensecIdSchema
from fastapi import HTTPException, status


class DeleteRepository(BaseRepository):
    
    def execute(self, censec_schema: TCensecIdSchema):
        
        try:
            # Montagem do sql
            sql = """ DELETE FROM T_CENSEC 
                      WHERE CENSEC_ID = :censec_id 
                      RETURNING CENSEC_ID"""

            # Preenchimento de parâmetros
            params = {
                "censec_id": censec_schema.censec_id
            }

            # Execução do sql
            response = self.run_and_return(sql, params)

            # Retorna o resultado
            return response
    
        except Exception as e:
            # Informa que houve uma falha na exclusão
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir T_CENSEC: {e}"
            )