from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_tb_cartorio_schema import TTbCartorioIdSchema
class TTbCartorioShowRepository(BaseRepository):
    def execute(self, cartorio_schema: TTbCartorioIdSchema):
        sql = """
            SELECT
                TB_CARTORIO_ID,
                DESCRICAO,
                MUNICIPIO_ID,
                DESCRICAO_MUNICIPIO,
                CNS
            FROM T_TB_CARTORIO
            WHERE TB_CARTORIO_ID = :tb_cartorio_id
        """
        params = {"tb_cartorio_id": cartorio_schema.tb_cartorio_id}
        return self.fetch_one(sql, params)
