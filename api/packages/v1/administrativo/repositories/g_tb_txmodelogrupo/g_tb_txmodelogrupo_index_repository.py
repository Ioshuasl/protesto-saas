from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

class IndexRepository(BaseRepository):
    """
    Repositório responsável por buscar todos os registros da tabela G_TB_TXMODELOGRUPO.
    """

    def execute(self):
        """
        Executa a operação de listagem de todos os registros na tabela G_TB_TXMODELOGRUPO.

        Returns:
            list: Uma lista de dicionários representando os registros encontrados.
        """
        try:
            # Montagem do SQL para buscar todos os registros da tabela G_TB_TXMODELOGRUPO
            sql = """
                SELECT
                    TB_TXMODELOGRUPO_ID,
                    DESCRICAO,
                    SITUACAO,
                    SISTEMA_ID
                FROM
                    G_TB_TXMODELOGRUPO
            """

            # Execução do SQL e retorno de todos os resultados
            response = self.fetch_all(sql)
            return response

        except Exception as e:
            # Em caso de erro, lança uma exceção HTTP detalhando o problema
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao buscar todos os registros de G_TB_TXMODELOGRUPO: {e}"
            )