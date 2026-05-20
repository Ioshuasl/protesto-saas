from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_tb_profissao_schema import GTbProfissaoIdSchema
from fastapi import HTTPException, status

class ShowRepository(BaseRepository):
    """
    Repositório para a operação de exibição de um registro na tabela G_TB_PROFISSAO.
    """

    def execute(self, profissao_schema: GTbProfissaoIdSchema):
        """
        Busca uma profissão específica pelo ID.

        Args:
            profissao_schema (GTbProfissaoIdSchema): O esquema que contém o ID do registro.

        Returns:
            O registro encontrado ou None se não existir.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:
            # Montagem do SQL
            sql = "SELECT * FROM G_TB_PROFISSAO WHERE TB_PROFISSAO_ID = :tb_profissao_id"

            # Preenchimento de parâmetros
            params = {
                'tb_profissao_id': profissao_schema.tb_profissao_id
            }

            # Execução do SQL
            result = self.fetch_one(sql, params)

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Profissão não encontrada"
                )

            return result
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao buscar profissão: {str(e)}"
            )