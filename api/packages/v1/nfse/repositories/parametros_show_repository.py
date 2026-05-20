from abstracts.repository import BaseRepository
from packages.v1.nfse.schemas.parametros_schema import ParametrosIdSchema


class ParametrosShowRepository(BaseRepository):
    def execute(self, data: ParametrosIdSchema):
        sql = """
            SELECT *
            FROM PARAMETROS
            WHERE ID_PARAMETROS = :id_parametros
        """
        return self.fetch_one(sql, {"id_parametros": data.id_parametros})

