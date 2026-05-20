from abstracts.repository import BaseRepository


class NfseIndexRepository(BaseRepository):
    def execute(self):
        sql = """
            SELECT
                ID_NFSE,
                DATA_HORA,
                NUMNFSE,
                DATAEMISSAO,
                TOTAL_SERVICOS,
                TOTAL_DEDUCOES,
                TOTAL_LIQUIDO,
                VALOR_ISS,
                TOMADOR_RAZAO_SOCIAL,
                TOMADOR_CNPJ,
                TOMADOR_EMAIL,
                TOMADOR_TELEFONE,
                ID_CLIENTE,
                ID_PARAMETROS
            FROM NFSE
            ORDER BY ID_NFSE DESC
        """
        return self.fetch_all(sql)
