from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_natureza_schema import GNaturezaDescricaoSchema

class GetByDescricaoRepository(BaseRepository):
    """
    Repositório para a operação de busca de um registro na tabela
    g_natureza por descrição.
    """

    def execute(self, natureza_schema: GNaturezaDescricaoSchema):
        """
        Executa a consulta SQL para buscar um registro pela descrição.

        Args:
            natureza_schema (GNaturezaDescricaoSchema): O esquema com a descrição a ser buscada.

        Returns:
            Um dicionário contendo os dados do registro ou None se não for encontrado.
        """
        # Montagem do SQL
        sql = """ SELECT * FROM G_NATUREZA WHERE DESCRICAO = :descricao """

        # Preenchimento de parâmetros
        params = {
            'descricao': natureza_schema.descricao
        }

        # Execução do sql
        return self.fetch_one(sql, params)