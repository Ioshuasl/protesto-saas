from abstracts.repository import BaseRepository


class FirebirdCheckAction(BaseRepository):

    def execute(self):
        
        # Montagem do SQL
        sql = """ SELECT 1 FROM RDB$DATABASE """

        # Execução do sql
        response = self.fetch_one(sql)

        if response:

            # Dados 
            response = {
                "status" : "Banco de dados acessível"
            }

        # Retorna os dados localizados
        return response