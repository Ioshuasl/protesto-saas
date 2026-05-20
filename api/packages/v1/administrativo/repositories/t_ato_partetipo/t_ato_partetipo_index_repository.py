from abstracts.repository import BaseRepository

class TAtoParteTipoIndexRepository(BaseRepository):
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
        sql = """ SELECT
                    TAP.ATO_PARTETIPO_ID,
                    TAP.DESCRICAO,
                    TAP.TIPO_PARTE,
                    TAP.AUTO_QUALIFICA,
                    TAP.DECLARA_DOI,
                    TAP.POSSUI_DOCUMENTO_EXT,
                    TAP.SITUACAO,
                    TAP.CENSEC_QUALIDADE_ID
                  FROM T_ATO_PARTETIPO TAP
              """

        # Execução do sql
        response = self.fetch_all(sql)

        # Retorna os dados localizados
        return response