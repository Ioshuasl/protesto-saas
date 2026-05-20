from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_servico_tipo_schema import TServicoTipoIdSchema
from fastapi import HTTPException, status


class DeleteRepository(BaseRepository):

    def execute(self, servico_tipo_schema: TServicoTipoIdSchema):

        try:
            # Montagem do sql
            sql = """ 
                    DELETE FROM T_SERVICO_TIPO 
                    WHERE SERVICO_TIPO_ID = :servico_tipo_id 
                    RETURNING SERVICO_TIPO_ID
                 """

            # Preenchimento de parâmetros
            params = {
                "servico_tipo_id": servico_tipo_schema.servico_tipo_id
            }

            # Execução do sql
            response = self.run_and_return(sql, params)

            # Retorna o resultado
            return response
    
        except Exception as e:
            # Informa que houve uma falha na exclusão
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir T_SERVICO_TIPO: {e}"
            )