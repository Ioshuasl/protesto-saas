from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_minuta_schema import TMinutaIdSchema
from fastapi import HTTPException, status


class DeleteRepository(BaseRepository):

    def execute(self, minuta_schema: TMinutaIdSchema):

        try:
            # Montagem do sql
            sql = """ 
                    DELETE FROM T_MINUTA 
                    WHERE MINUTA_ID = :minuta_id 
                    RETURNING MINUTA_ID
                 """

            # Preenchimento de parâmetros
            params = {
                "minuta_id": minuta_schema.minuta_id
            }

            # Execução do sql
            response = self.run_and_return(sql, params)

            # Retorna o resultado
            return response
    
        except Exception as e:
            # Informa que houve uma falha na exclusão
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir T_MINUTA: {e}"
            )