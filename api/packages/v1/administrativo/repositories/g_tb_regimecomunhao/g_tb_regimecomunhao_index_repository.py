from abstracts.repository import BaseRepository

class IndexRepository(BaseRepository):

    def execute(self):
        """
        Executa a operação de listagem de todos os registros na tabela
        g_tb_regimecomunhao.
        """

        # Montagem do sql
        sql = """ SELECT TB_REGIMECOMUNHAO_ID,
                         DESCRICAO,                         
                         SITUACAO,
                         TB_REGIMEBENS_ID
      FROM G_TB_REGIMECOMUNHAO """

        # Execução do sql
        response = self.fetch_all(sql)

        # Retorna os dados localizados
        return response