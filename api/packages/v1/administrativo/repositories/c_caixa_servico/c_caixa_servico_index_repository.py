from abstracts.repository import BaseRepository

class IndexRepository(BaseRepository):

    def execute(self):

        # Montagem do sql
        sql = """ SELECT * FROM c_caixa_servico """

        # Execução do sql
        response = self.fetch_all(sql)

        # Retorna os dados localizados
        return response