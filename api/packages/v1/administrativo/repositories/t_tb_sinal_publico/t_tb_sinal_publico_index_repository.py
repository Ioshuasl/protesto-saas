from abstracts.repository import BaseRepository


class TTbSinalPublicoIndexRepository(BaseRepository):
    def execute(self):
        sql = """
            SELECT
                TB_SINALPUBLICO_ID,
                DESCRICAO,
                SITUACAO
            FROM T_TB_SINALPUBLICO
            ORDER BY TB_SINALPUBLICO_ID
        """

        return self.fetch_all(sql)
