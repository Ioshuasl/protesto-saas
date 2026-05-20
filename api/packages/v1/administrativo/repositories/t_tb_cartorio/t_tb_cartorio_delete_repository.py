from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_tb_cartorio_schema import TTbCartorioIdSchema
class TTbCartorioDeleteRepository(BaseRepository):
    def execute(self, cartorio_schema: TTbCartorioIdSchema):
        sql = """
            DELETE FROM T_TB_CARTORIO
            WHERE TB_CARTORIO_ID = :tb_cartorio_id
        """
        params = {"tb_cartorio_id": cartorio_schema.tb_cartorio_id}
        self.run(sql, params)
        return {"tb_cartorio_id": cartorio_schema.tb_cartorio_id}
