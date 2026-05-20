from abstracts.repository import BaseRepository

class IndexRepository(BaseRepository):
    """
    Repositório para a operação de listagem de todos os registros
    na tabela G_TB_ESTADOCIVIL.
    """
    
    def execute(self):
        """
        Executa a consulta SQL para buscar todos os registros.

        Returns:
            Uma lista de dicionários contendo os dados dos registros.
        """
        # Montagem do SQL
        sql = """ SELECT * FROM G_TB_ESTADOCIVIL """

        # Execução do sql
        response = self.fetch_all(sql)

        # Retorna os dados localizados
        return response