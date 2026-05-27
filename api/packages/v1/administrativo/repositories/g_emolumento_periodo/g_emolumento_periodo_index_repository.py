from abstracts.repository import BaseRepository

class GEmolumentoPeriodoIndexRepository(BaseRepository):
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
                    GEP.*
                  FROM G_EMOLUMENTO_PERIODO GEP
              ORDER BY GEP.EMOLUMENTO_PERIODO_ID DESC
            """

        # Execução do sql
        response = self.fetch_all(sql)

        # Retorna os dados localizados
        return response