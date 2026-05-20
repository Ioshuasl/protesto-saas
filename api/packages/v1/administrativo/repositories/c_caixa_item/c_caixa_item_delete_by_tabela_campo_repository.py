from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.c_caixa_item_schema import CaixaItemSchema


class CaixaItemDeleteByTabelaCampoRepository(BaseRepository):

    def execute(self, data: CaixaItemSchema):
        sql = """
            DELETE FROM
                C_CAIXA_ITEM CCI
            WHERE
                CCI.CAIXA_ITEM_ID = (
                    SELECT
                        FIRST 1
                        CCI2.CAIXA_ITEM_ID
                    FROM
                        C_CAIXA_ITEM CCI2
                    WHERE
                        CCI2.TABELA = :tabela
                        AND CCI2.CAMPO_ID = :campo_id
                    ORDER BY
                        CCI2.CAIXA_ITEM_ID DESC
                )
            RETURNING
                CCI.CAIXA_ITEM_ID AS caixa_item_id
        """

        params = {
            "tabela": data.tabela,
            "campo_id": data.campo_id,
        }

        return self.run_and_return(sql, params)
