from abstracts.repository import BaseRepository
from packages.v1.nfse.schemas.nfse_schema import NfseIdSchema


class NfseShowRepository(BaseRepository):
    def execute(self, data: NfseIdSchema):
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
            WHERE ID_NFSE = :id_nfse
        """
        return self.fetch_one(sql, {"id_nfse": data.id_nfse})
