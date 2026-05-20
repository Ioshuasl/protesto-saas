from abstracts.repository import BaseRepository

class IndexRepository(BaseRepository):
    """
    Repositório para a operação de listagem de todos os registros
    na tabela T_SERVICO_ETIQUETA.
    """
    
    def execute(self):
        """
        Executa a consulta SQL para buscar todos os registros.

        Returns:
            Uma lista de dicionários contendo os dados dos registros.
        """
        # Montagem do SQL
        # Tabela e colunas ajustadas para T_SERVICO_ETIQUETA
        sql = """ 
            SELECT 
                SERVICO_ETIQUETA_ID,
                ETIQUETA_MODELO_ID,
                SERVICO_TIPO_ID 
            FROM T_SERVICO_ETIQUETA 
        """

        # Execução do sql
        response = self.fetch_all(sql)

        # Retorna os dados localizados
        return response