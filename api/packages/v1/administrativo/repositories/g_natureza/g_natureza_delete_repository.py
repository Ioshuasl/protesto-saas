from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_natureza_schema import GNaturezaIdSchema
from fastapi import HTTPException, status


class DeleteRepository(BaseRepository):

    def execute(self, natureza_schema: GNaturezaIdSchema):

        try:
            # Montagem do sql
            sql = """ DELETE FROM G_NATUREZA 
                      WHERE NATUREZA_ID = :natureza_id 
                      RETURNING NATUREZA_ID
                """

            # Preenchimento de parâmetros
            params = {
                "natureza_id": natureza_schema.natureza_id
            }

            # Execução do sql
            response = self.run_and_return(sql, params)

            # Retorna o resultado
            return response
    
        except Exception as e:
            # Informa que houve uma falha na exclusão
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir G_NATUREZA: {e}"
            )