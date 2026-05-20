from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_censec_naturezalitigio_schema import TCensecNaturezalitigioIdSchema
from fastapi import HTTPException, status


class DeleteRepository(BaseRepository):
    
    def execute(self, censec_naturezalitigio_schema: TCensecNaturezalitigioIdSchema):
        
        try:
            # Montagem do sql
            sql = """ DELETE FROM T_CENSEC_NATUREZALITIGIO 
                      WHERE CENSEC_NATUREZALITIGIO_ID = :censec_naturezalitigio_id 
                      RETURNING CENSEC_NATUREZALITIGIO_ID
                """

            # Preenchimento de parâmetros
            params = {
                "censec_naturezalitigio_id": censec_naturezalitigio_schema.censec_naturezalitigio_id
            }

            # Execução do sql
            response = self.run_and_return(sql, params)

            # Retorna o resultado
            return response
    
        except Exception as e:
            # Informa que houve uma falha na exclusão
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir T_CENSEC_NATUREZALITIGIO: {e}"
            )