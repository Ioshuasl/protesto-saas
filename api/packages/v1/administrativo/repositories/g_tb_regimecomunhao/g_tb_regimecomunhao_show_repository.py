from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_tb_regimecomunhao_schema import GTbRegimecomunhaoIdSchema

class ShowRepository(BaseRepository):

    def execute(self, regimecomunhao_schema: GTbRegimecomunhaoIdSchema):

        # Montagem do sql
        sql = """ SELECT * FROM G_TB_REGIMECOMUNHAO WHERE TB_REGIMECOMUNHAO_ID = :tb_regimecomunhao_id """

        # Preenchimento de parâmetros
        params = {
            'tb_regimecomunhao_id' : regimecomunhao_schema.tb_regimecomunhao_id
        }

        # Execução do sql
        return self.fetch_one(sql, params)