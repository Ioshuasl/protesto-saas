from packages.v1.administrativo.schemas.c_caixa_item_schema import CaixaItemSchema
from abstracts.repository import BaseRepository


class Show(BaseRepository):

    def execute(self, caixa_item_schema: CaixaItemSchema):

        # Montagem do SQL
        sql = """ SELECT * FROM c_caixa_item cci WHERE cci.caixa_item_id = :caixaItemId """

        # Preenchimento dos parâmetros
        params = {
            "caixaItemId" : caixa_item_schema.caixa_item_id
        }

        # Execução do sql
        response = self.fetch_one(sql, params)

        # Retorna a informação localizada
        return response