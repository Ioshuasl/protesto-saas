from abstracts.repository import BaseRepository


class GEmolumentoIndexRepository(BaseRepository):
    """
    Repositório para a operação de listagem de todos os registros
    na tabela t_censec_qualidade.
    """

    def execute(self):
        """
        Executa a consulta SQL para buscar todos os registros.

        Returns:
            Uma lista de dicionários contendo os dados dos registros.
        """
        # Montagem do SQL
        sql = """ SELECT
                    GE.*
                  FROM G_EMOLUMENTO GE
            """

        # Execução do sql
        response = self.fetch_all(sql)

        # Retorna os dados localizados
        return response
