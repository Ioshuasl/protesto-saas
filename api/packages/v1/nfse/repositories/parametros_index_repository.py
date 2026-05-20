from abstracts.repository import BaseRepository


class ParametrosIndexRepository(BaseRepository):
    def execute(self):
        sql = """
            SELECT *
            FROM PARAMETROS
            ORDER BY ID_PARAMETROS
        """
        return self.fetch_all(sql)

