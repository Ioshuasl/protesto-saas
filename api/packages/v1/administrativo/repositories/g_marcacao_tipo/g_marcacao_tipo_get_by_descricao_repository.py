from abstracts.repository import BaseRepository

# O schema de entrada deve ser o de descrição para a tabela G_MARCACAO_TIPO
from packages.v1.administrativo.schemas.g_marcacao_tipo_schema import (
    GMarcacaoTipoDescricaoSchema,
)


class GMarcacaoTipoGetByDescricaoRepository(BaseRepository):
    """
    Repositório para a operação de busca de um registro na tabela
    G_MARCACAO_TIPO por descrição.
    """

    def execute(self, marcacao_tipo_schema: GMarcacaoTipoDescricaoSchema):
        """
        Executa a consulta SQL para buscar um registro pela descrição.

        Args:
            marcacao_tipo_schema (GMarcacaoTipoDescricaoSchema): O esquema com a descrição a ser buscada.

        Returns:
            Um dicionário contendo os dados do registro ou None se não for encontrado.
        """
        # Montagem do SQL
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
                  FROM G_MARCACAO_TIPO WHERE DESCRICAO = :descricao """

        # Preenchimento de parâmetros
        params = {"descricao": marcacao_tipo_schema.descricao}

        # Execução do sql
        return self.fetch_one(sql, params)
