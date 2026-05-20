from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_tb_bairro_schema import GTbBairroIdSchema
from fastapi import HTTPException, status

class ShowRepository(BaseRepository):
    """
    Repositório para a operação de exibição de um registro na tabela g_tb_bairro.
    """

    def execute(self, bairro_schema: GTbBairroIdSchema):
        """
        Busca um registro específico de Bairro pelo ID.

        Args:
            bairro_schema (GTbBairroIdSchema): O esquema que contém o ID do registro.

        Returns:
            O registro encontrado ou None se não existir.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:
            # Montagem do SQL
            sql = "SELECT * FROM G_TB_BAIRRO WHERE TB_BAIRRO_ID = :tb_bairro_id"

            # Preenchimento de parâmetros
            params = {
                'tb_bairro_id': bairro_schema.tb_bairro_id
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