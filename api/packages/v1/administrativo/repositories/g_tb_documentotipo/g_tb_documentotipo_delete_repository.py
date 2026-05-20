from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_tb_documentotipo_schema import GTbDocumentoTipoIdSchema
from fastapi import HTTPException, status


class DeleteRepository(BaseRepository):

    def execute(self, documento_tipo_schema: GTbDocumentoTipoIdSchema):

        try:
            # Montagem do sql
            sql = """ DELETE FROM G_TB_DOCUMENTOTIPO 
                      WHERE TB_DOCUMENTOTIPO_ID = :tb_documentotipo_id 
                      RETURNING TB_DOCUMENTOTIPO_ID
                """

            # Preenchimento de parâmetros
            params = {
                "tb_documentotipo_id": documento_tipo_schema.tb_documentotipo_id
            }

            # Execução do sql
            response = self.run_and_return(sql, params)

            # Retorna o resultado
            return response
    
        except Exception as e:
            # Informa que houve uma falha na exclusão
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir G_TB_DOCUMENTOTIPO: {e}"
            )