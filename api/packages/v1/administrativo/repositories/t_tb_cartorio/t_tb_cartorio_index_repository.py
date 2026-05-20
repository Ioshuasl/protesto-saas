from abstracts.repository import BaseRepository
class TTbCartorioIndexRepository(BaseRepository):
    def execute(self):
        sql = """
            SELECT
                TB_CARTORIO_ID,
                DESCRICAO,
                MUNICIPIO_ID,
                DESCRICAO_MUNICIPIO,
                CNS
            FROM T_TB_CARTORIO
            ORDER BY DESCRICAO
        """
        return self.fetch_all(sql)
