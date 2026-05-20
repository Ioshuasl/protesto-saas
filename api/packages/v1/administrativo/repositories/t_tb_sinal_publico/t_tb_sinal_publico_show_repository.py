from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_tb_sinal_publico_schema import (
    TTbSinalPublicoIdSchema,
)


class TTbSinalPublicoShowRepository(BaseRepository):
    def execute(self, sinal_publico_schema: TTbSinalPublicoIdSchema):
        sql = """
            SELECT
                TB_SINALPUBLICO_ID,
                DESCRICAO,
                SITUACAO
            FROM T_TB_SINALPUBLICO
            WHERE TB_SINALPUBLICO_ID = :tb_sinalpublico_id
        """

        params = {"tb_sinalpublico_id": sinal_publico_schema.tb_sinalpublico_id}
        return self.fetch_one(sql, params)
