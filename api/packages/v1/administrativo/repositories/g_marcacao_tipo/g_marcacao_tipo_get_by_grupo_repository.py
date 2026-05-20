from abstracts.repository import BaseRepository

# O schema de entrada deve ser o de descrição para a tabela G_MARCACAO_TIPO
from actions.data.sql_string_builder import SqlStringBuilder
from packages.v1.administrativo.schemas.g_marcacao_tipo_schema import (
    GMarcacaoTipoGrupoSchema,
)


class GMarcacaoTipoGetByGrupoRepository(BaseRepository):
    """
    Repositório para a operação de busca de um registro na tabela
    G_MARCACAO_TIPO por descrição.
    """

    def execute(self, marcacao_tipo_schema: GMarcacaoTipoGrupoSchema):
        """
        Executa a consulta SQL para buscar um registro pela descrição.

        Args:
            marcacao_tipo_schema (GMarcacaoTipoGrupoSchema): O esquema com os filtros a serem consultados.

        Returns:
            Um dicionário contendo os dados do registro ou None se não for encontrado.
        """

        grupo = SqlStringBuilder.to_in_clause(marcacao_tipo_schema.grupo)

        # Montagem do SQL
        sql = f""" SELECT marcacao_tipo_id,
                    descricao,
                    nome,
                    grupo,
                    situacao,
                    sistema_id,
                    grupo_tipo,
                    tipo_qualificacao,
                    condicao_sql,
                    separador_1,
                    separador_2,
                    separador_3,
                    tipo_valor,
                    atualizar,
                    protegida,
                    ativar_separador,
                    sql_completo
                FROM g_marcacao_tipo
                WHERE grupo in ({grupo})
                    AND sistema_id = :sistema_id
                    AND situacao = :situacao  """

        # Preenchimento de parâmetros
        params = {
            "sistema_id": marcacao_tipo_schema.sistema_id,
            "situacao": marcacao_tipo_schema.situacao,
        }

        # Execução do sql
        return self.fetch_all(sql, params)
