from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_tb_estadocivil_schema import GTbEstadoCivilIdSchema
from fastapi import HTTPException, status

class DeleteRepository(BaseRepository):

    def execute(self, estadocivil_schema: GTbEstadoCivilIdSchema):

        try:
            # Montagem do sql
            sql = """ DELETE FROM G_TB_ESTADOCIVIL 
                       WHERE TB_ESTADOCIVIL_ID = :tb_estadocivil_id 
                       RETURNING TB_ESTADOCIVIL_ID
                """

            # Preenchimento de parâmetros
            params = {
                "tb_estadocivil_id": estadocivil_schema.tb_estadocivil_id
            }

            # Execução do sql
            response = self.run_and_return(sql, params)

            # Retorna o resultado
            return response
    
        except Exception as e:
            # Informa que houve uma falha na exclusão
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir G_TB_ESTADOCIVIL: {e}"
            )