from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.c_caixa_item_schema import CaixaItemSchema


class CaixaItemShowByTabelaCampoRepository(BaseRepository):

    def execute(self, data: CaixaItemSchema):
        sql = """
            SELECT
                FIRST 1
                CCI.*
            FROM
                C_CAIXA_ITEM CCI
            WHERE
                CCI.TABELA = :tabela
                AND CCI.CAMPO_ID = :campo_id
            ORDER BY
                CCI.CAIXA_ITEM_ID DESC
        """

        params = {
            "tabela": data.tabela,
            "campo_id": data.campo_id,
        }

        return self.fetch_one(sql, params)
