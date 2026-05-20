from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_cidade_schema import GCidadeNomeSchema

class GetByNomeRepository(BaseRepository):
    """
    Repositório para a operação de busca de um registro na tabela
    G_CIDADE por nome (CIDADE_NOME).
    """

    def execute(self, g_cidade_schema: GCidadeNomeSchema):
        """
        Executa a consulta SQL para buscar um registro pelo nome da cidade.

        Args:
            g_cidade_schema (GCidadeNomeSchema): O esquema com o nome da cidade a ser buscada.

        Returns:
            Um dicionário contendo os dados do registro ou None se não for encontrado.
        """
        # Montagem do SQL
        sql = """ SELECT * FROM G_CIDADE WHERE CIDADE_NOME = :cidade_nome """

        # Preenchimento de parâmetros
        params = {
            'cidade_nome': g_cidade_schema.cidade_nome
        }

        # Execução do sql
        return self.fetch_one(sql, params)