from abstracts.repository import BaseRepository

class IndexRepository(BaseRepository):
    """
    Repositório para a operação de listagem de todos os registros
    na tabela t_minuta.
    """

    def execute(self):
        """
        Executa a consulta SQL para buscar todos os registros.

        Returns:
            Uma lista de dicionários contendo os dados dos registros.
        """
        # Montagem do SQL
        sql = """ SELECT TM.MINUTA_ID,
                         TM.ATO_TIPO_ID,
                         TM.NATUREZA_ID,
                         TM.DESCRICAO,
                         TM.PROTEGIDA,
                         TM.SITUACAO
                    FROM T_MINUTA TM
                    ORDER BY TM.MINUTA_ID ASC"""

        # Execução do sql
        response = self.fetch_all(sql)

        # Retorna os dados localizados
        return response