from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_cidade_schema import GCidadeIdSchema
from fastapi import HTTPException, status


class DeleteRepository(BaseRepository):

    def execute(self, g_cidade_schema: GCidadeIdSchema):

        try:
            # Montagem do sql
            sql = """ DELETE FROM G_CIDADE 
                      WHERE CIDADE_ID = :cidade_id 
                      RETURNING CIDADE_ID"""

            # Preenchimento de parâmetros
            params = {
                "cidade_id": g_cidade_schema.cidade_id
            }

            # Execução do sql
            response = self.run_and_return(sql, params)

            # Retorna o resultado
            return response
    
        except Exception as e:
            # Informa que houve uma falha na exclusão
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir G_CIDADE: {e}"
            )