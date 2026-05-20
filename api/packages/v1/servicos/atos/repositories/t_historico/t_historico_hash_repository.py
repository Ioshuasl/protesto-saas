from abstracts.repository import BaseRepository
from packages.v1.servicos.atos.schemas.t_historico_schema import THistoricoHashSchema


class THistoricoHashRepository(BaseRepository):
    def execute(self, data: THistoricoHashSchema):
        sql = """
            SELECT
                TH.*
            FROM T_HISTORICO TH
            WHERE TH.HASH LIKE :hash
            ORDER BY TH.DATA DESC
        """

        params = {"hash": data.hash}

        return self.fetch_all(sql, params)
