from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_marcacao_tipo_schema import (
    GMarcacaoTipoNomeSchema,
)


class GMarcacaoTipoGetByNomeRepository(BaseRepository):
    """
    Repositório para a operação de busca de um registro na tabela
    G_MARCACAO_TIPO por descrição.
    """

    def execute(self, marcacao_tipo_schema: GMarcacaoTipoNomeSchema):
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
                         TEXTO,
                         TIPO_VALOR
                  FROM G_MARCACAO_TIPO
                  WHERE NOME LIKE :nome
                  AND SISTEMA_ID = :sistema_id """

        # Preenchimento de parâmetros
        params = {
            "nome": marcacao_tipo_schema.nome,
            "sistema_id": marcacao_tipo_schema.sistema_id,
        }

        # Execução do sql
        return self.fetch_one(sql, params)
