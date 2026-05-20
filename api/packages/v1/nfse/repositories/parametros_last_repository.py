from abstracts.repository import BaseRepository


class ParametrosLastRepository(BaseRepository):
    def execute(self):
        sql = """
            SELECT FIRST 1 *
            FROM PARAMETROS
            ORDER BY ID_PARAMETROS DESC
        """
        return self.fetch_one(sql)

