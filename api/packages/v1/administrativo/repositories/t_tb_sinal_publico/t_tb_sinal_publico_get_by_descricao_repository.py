from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_tb_sinal_publico_schema import (
    TTbSinalPublicoDescricaoSchema,
)


class TTbSinalPublicoGetByDescricaoRepository(BaseRepository):
    def execute(self, sinal_publico_schema: TTbSinalPublicoDescricaoSchema):
        sql = """
            SELECT
                TB_SINALPUBLICO_ID,
                DESCRICAO,
                SITUACAO
            FROM T_TB_SINALPUBLICO
            WHERE DESCRICAO = :descricao
        """

        params = {"descricao": sinal_publico_schema.descricao}
        return self.fetch_one(sql, params)
