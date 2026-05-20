from abstracts.repository import BaseRepository
from packages.v1.parametros.schemas.g_config_schema import GConfigIndexFilterSchema


class GConfigIndexRepository(BaseRepository):
    def execute(self, data: GConfigIndexFilterSchema):
        sql = """
            SELECT
                GC.CONFIG_ID,
                GC.CONFIG_GRUPO_ID,
                GC.CONFIG_PADRAO_ID,
                GC.SECAO,
                GC.NOME,
                GC.VALOR,
                GC.DESCRICAO,
                GC.TERMINAL,
                GC.TIPO_VALOR,
                GC.ATUALIZADO
            FROM G_CONFIG GC
            JOIN G_CONFIG_GRUPO GCG ON GC.CONFIG_GRUPO_ID = GCG.CONFIG_GRUPO_ID
            JOIN G_SISTEMA GS ON GCG.SISTEMA_ID = GS.SISTEMA_ID
            WHERE GS.SISTEMA_ID = :sistema_id
              AND GC.SECAO LIKE :secao
              AND GCG.DESCRICAO LIKE :descricao
            ORDER BY CONFIG_ID
        """

        params = {
            "sistema_id": data.sistema_id,
            "secao": f"%{data.secao}%",
            "descricao": f"%{data.descricao}%",
        }

        return self.fetch_all(sql, params)