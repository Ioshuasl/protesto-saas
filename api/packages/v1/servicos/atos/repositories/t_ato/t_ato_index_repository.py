from abstracts.repository import BaseRepository


class TAtoIndexRepository(BaseRepository):
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
        sql = """
                SELECT
                    TA.ATO_ID,
                    TA.SITUACAO_ATO,
                    TA.PROTOCOLO,
                    TAT.DESCRICAO,
                    TA.DATA_LAVRATURA,
                    TA.DATA_ABERTURA,
                    TLA.NUMERO_LIVRO,
                    TA.FOLHA_INICIAL,
                    TA.FOLHA_FINAL,
                    TA.ATO_TIPO_ID
                FROM
                    T_ATO TA
                LEFT JOIN T_LIVRO_ANDAMENTO tla ON TA.LIVRO_ANDAMENTO_ID = TLA.LIVRO_ANDAMENTO_ID
                LEFT JOIN T_ATO_TIPO TAT ON TA.ATO_TIPO_ID = TAT.ATO_TIPO_ID
                ORDER BY
                    TA.ATO_ID DESC
            """

        # Execução do sql
        response = self.fetch_all(sql)

        # Retorna os dados localizados
        return response
