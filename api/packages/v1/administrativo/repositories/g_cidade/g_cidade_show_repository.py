from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_cidade_schema import GCidadeIdSchema
from fastapi import HTTPException, status

class ShowRepository(BaseRepository):
    """
    Repositório para a operação de exibição de um registro na tabela G_CIDADE.
    """

    def execute(self, g_cidade_schema: GCidadeIdSchema):
        """
        Busca um registro específico de G_CIDADE pelo ID (CIDADE_ID).

        Args:
            g_cidade_schema (GCidadeIdSchema): O esquema que contém o ID do registro.

        Returns:
            O registro encontrado ou None se não existir.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:
            # Montagem do SQL
            sql = "SELECT * FROM G_CIDADE WHERE CIDADE_ID = :cidade_id"

            # Preenchimento de parâmetros
            params = {
                'cidade_id': g_cidade_schema.cidade_id
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