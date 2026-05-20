from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_medida_tipo_schema import GMedidaTipoIdSchema
from fastapi import HTTPException, status


class DeleteRepository(BaseRepository):

    def execute(self, medida_tipo_schema: GMedidaTipoIdSchema):

        try:
            # Montagem do sql
            sql = """ DELETE FROM G_MEDIDA_TIPO 
                      WHERE MEDIDA_TIPO_ID = :medida_tipo_id 
                      RETURNING MEDIDA_TIPO_ID
                  """

            # Preenchimento de parâmetros
            params = {
                "medida_tipo_id": medida_tipo_schema.medida_tipo_id
            }

            # Execução do sql
            response = self.run_and_return(sql, params)

            # Retorna o resultado
            return response
    
        except Exception as e:
            # Informa que houve uma falha na exclusão
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir G_MEDIDA_TIPO: {e}"
            )