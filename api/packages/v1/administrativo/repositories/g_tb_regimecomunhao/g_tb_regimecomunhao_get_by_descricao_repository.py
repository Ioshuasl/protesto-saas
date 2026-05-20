from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_tb_regimecomunhao_schema import GTbRegimecomunhaoDescricaoSchema

class GetByDescricaoRepository(BaseRepository):

    def execute(self, regimecomunhao_schema: GTbRegimecomunhaoDescricaoSchema):

        # Montagem do sql
        sql = """ SELECT * FROM G_TB_REGIMECOMUNHAO WHERE DESCRICAO = :descricao """

        # Preenchimento de parâmetros
        params = {
            'descricao': regimecomunhao_schema.descricao
        }

        # Execução do sql
        return self.fetch_one(sql, params)