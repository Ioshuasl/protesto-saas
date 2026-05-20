from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_tb_regimebens_schema import GTbRegimebensIdSchema
from fastapi import HTTPException, status

class ShowRepository(BaseRepository):
    """
    Repositório para a operação de exibição de um registro na tabela g_tb_regimebens.
    """

    def execute(self, regimebens_schema: GTbRegimebensIdSchema):
        """
        Busca um tipo de regime de bens específico pelo ID.

        Args:
            regimebens_schema (GTbRegimebensIdSchema): O esquema que contém o ID do registro.

        Returns:
            O registro encontrado ou None se não existir.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:
            # Montagem do SQL
            sql = "SELECT * FROM G_TB_REGIMEBENS WHERE TB_REGIMEBENS_ID = :tb_regimebens_id"

            # Preenchimento de parâmetros
            params = {
                'tb_regimebens_id': regimebens_schema.tb_regimebens_id
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