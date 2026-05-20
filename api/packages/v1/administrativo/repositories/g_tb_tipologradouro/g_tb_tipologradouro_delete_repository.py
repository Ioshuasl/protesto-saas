from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_tb_tipologradouro_schema import GTbTipoLogradouroIdSchema
from fastapi import HTTPException, status


class DeleteRepository(BaseRepository):

    def execute(self, tipologradouro_schema: GTbTipoLogradouroIdSchema):

        try:
            # Montagem do sql
            sql = """ 
                    DELETE FROM G_TB_TIPOLOGRADOURO 
                    WHERE TB_TIPOLOGRADOURO_ID = :tipologradouro_id 
                    RETURNING TB_TIPOLOGRADOURO_ID
                """

            # Preenchimento de parâmetros
            params = {
                "tipologradouro_id": tipologradouro_schema.tb_tipologradouro_id
            }

            # Execução do sql
            response = self.run_and_return(sql, params)

            # Retorna o resultado
            return response
    
        except Exception as e:
            # Informa que houve uma falha na exclusão
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir G_TB_TIPOLOGRADOURO: {e}"
            )