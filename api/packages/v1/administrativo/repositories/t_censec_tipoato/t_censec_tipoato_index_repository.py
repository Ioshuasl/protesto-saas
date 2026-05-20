from abstracts.repository import BaseRepository

class TCensecTipoAtoIndexRepository(BaseRepository):
    """
    Repositório para a operação de listagem de todos os registros
    na tabela t_censec_qualidade.
    """
    
    def execute(self):
        """
        Executa a consulta SQL para buscar todos os registros.

        Returns:
            Uma lista de dicionários contendo os dados dos registros.
        """
        # Montagem do SQL
        sql = """ SELECT * FROM T_CENSEC_TIPOATO """

        # Execução do sql
        response = self.fetch_all(sql)

        # Retorna os dados localizados
        return response