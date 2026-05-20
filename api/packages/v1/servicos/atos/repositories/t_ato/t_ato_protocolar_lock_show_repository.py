from abstracts.repository import BaseRepository
from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoIdSchema


class TAtoProtocolarLockShowRepository(BaseRepository):
    def execute(self, data: TAtoIdSchema):
        sql = """
            SELECT TA.ATO_ID AS ato_id, TA.PROTOCOLO AS protocolo
            FROM T_ATO TA
            WHERE TA.ATO_ID = :ato_id
        """
        return self.fetch_one(sql, {"ato_id": data.ato_id})
