from abstracts.repository import BaseRepository
from fastapi import HTTPException, status


class GIbgePaisIndexRepository(BaseRepository):
    """
    Repositório para a operação de listagem de todos os registros
    na tabela G_IBGE_PAIS.
    """

    def execute(self):
        """
        Executa a consulta SQL para buscar todos os registros.

        Returns:
            Uma lista de dicionários contendo os dados dos registros.
        """
        try:
            # Montagem do SQL
            sql = """
                SELECT
                    GIP.*
                FROM G_IBGE_PAIS GIP
                WHERE GIP.COD_PAIS IS NOT NULL
            """

            # Execução do sql
            response = self.fetch_all(sql)

            # Retorna os dados localizados
            return response

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao listar registros de G_IBGE_PAIS: {e}",
            )
