from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_tb_estadocivil_schema import GTbEstadoCivilIdSchema
from fastapi import HTTPException, status

class ShowRepository(BaseRepository):
    """
    Repositório para a operação de exibição de um registro na tabela G_TB_ESTADOCIVIL.
    """

    def execute(self, estado_civil_schema: GTbEstadoCivilIdSchema):
        """
        Busca um registro específico de Estado Civil pelo ID.

        Args:
            estado_civil_schema (GTBEstadoCivilIdSchema): O esquema que contém o ID do registro.

        Returns:
            O registro encontrado ou None se não existir.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:
            # Montagem do SQL
            sql = "SELECT * FROM G_TB_ESTADOCIVIL WHERE TB_ESTADOCIVIL_ID = :tb_estadocivil_id"

            # Preenchimento de parâmetros
            params = {
                'tb_estadocivil_id': estado_civil_schema.tb_estadocivil_id
            }

            # Execução do SQL
            result = self.fetch_one(sql, params)

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Registro não encontrado"
                )

            return result
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao buscar registro: {str(e)}"
            )