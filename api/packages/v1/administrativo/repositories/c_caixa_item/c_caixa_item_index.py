from abstracts.repository import BaseRepository


class Index(BaseRepository):

    def execute(self):

        # Montagem do SQL
        sql = """ SELECT FIRST 10 * FROM c_caixa_item ORDER BY caixa_item_id DESC """

        # Execução do sql
        response = self.fetch_all(sql)

        # Retorna os dados localizados
        return response
