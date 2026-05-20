from abstracts.repository import BaseRepository

class IndexRepository(BaseRepository):
    """
    Repositório para a operação de listagem de todos os registros
    na tabela G_TB_DOCUMENTOTIPO.
    """
    
    def execute(self):
        """
        Executa a consulta SQL para buscar todos os registros.

        Returns:
            Uma lista de dicionários contendo os dados dos registros.
        """
        # Montagem do SQL
        sql = """ SELECT TB_DOCUMENTOTIPO_ID,
                         DESCRICAO,
                         SITUACAO,
                         POSSUI_NUMERACAO,
                         ORGAO_PADRAO,
                         DESCRICAO_SIMPLIFICADA,
                         TIPO,
                         DESCRICAO_SINTER 
                 FROM G_TB_DOCUMENTOTIPO """

        # Execução do sql
        response = self.fetch_all(sql)

        # Retorna os dados localizados
        return response