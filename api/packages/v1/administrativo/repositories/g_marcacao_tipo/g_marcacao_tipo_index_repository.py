from abstracts.repository import BaseRepository


class GMarcacaoTipoIndexRepository(BaseRepository):
    """
    Repositório para a operação de listagem de todos os registros
    na tabela G_MARCACAO_TIPO.
    """

    def execute(self):
        """
        Executa a consulta SQL para buscar todos os registros.

        Returns:
            Uma lista de dicionários contendo os dados dos registros.
        """
        # Montagem do SQL
        # Tabela ajustada para G_MARCACAO_TIPO
        sql = """ SELECT MARCACAO_TIPO_ID,
                         DESCRICAO,
                         NOME,
                         GRUPO,
                         SITUACAO,
                         SISTEMA_ID,
                         GRUPO_TIPO,
                         TIPO_QUALIFICACAO,
                         CONDICAO_SQL,
                         SEPARADOR_1,
                         SEPARADOR_2,
                         SEPARADOR_3,
                         TIPO_VALOR,
                         ATUALIZAR,
                         PROTEGIDA,
                         ATIVAR_SEPARADOR,
                         SQL_COMPLETO
                  FROM G_MARCACAO_TIPO """

        # Execução do sql
        response = self.fetch_all(sql)

        # Retorna os dados localizados
        return response
