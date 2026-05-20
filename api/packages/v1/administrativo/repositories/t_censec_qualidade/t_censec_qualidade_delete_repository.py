from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_censec_qualidade_schema import TCensecQualidadeIdSchema
from fastapi import HTTPException, status


class DeleteRepository(BaseRepository):
    
    def execute(self, censec_qualidade_schema: TCensecQualidadeIdSchema):
        
        try:
            # Montagem do sql
            sql = """ 
                    DELETE FROM T_CENSEC_QUALIDADE 
                    WHERE CENSEC_QUALIDADE_ID = :censec_qualidade_id 
                    RETURNING CENSEC_QUALIDADE_ID
                """

            # Preenchimento de parâmetros
            params = {
                "censec_qualidade_id": censec_qualidade_schema.censec_qualidade_id
            }

            # Execução do sql
            response = self.run_and_return(sql, params)

            # Retorna o resultado
            return response
    
        except Exception as e:
            # Informa que houve uma falha na exclusão
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir T_CENSEC_QUALIDADE: {e}"
            )