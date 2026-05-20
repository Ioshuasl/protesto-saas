from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_medida_tipo_schema import GMedidaTipoDescricaoSchema

class GetByDescricaoRepository(BaseRepository):
    """
    Repositório para a operação de busca de um registro na tabela
    g_medida_tipo por descrição.
    """

    def execute(self, medida_tipo_schema: GMedidaTipoDescricaoSchema):
        """
        Executa a consulta SQL para buscar um registro pela descrição.

        Args:
            medida_tipo_schema (GMedidaTipoDescricaoSchema): O esquema com a descrição a ser buscada.

        Returns:
            Um dicionário contendo os dados do registro ou None se não for encontrado.
        """
        # Montagem do SQL
        sql = """ SELECT * FROM G_MEDIDA_TIPO WHERE DESCRICAO = :descricao """

        # Preenchimento de parâmetros
        params = {
            'descricao': medida_tipo_schema.descricao
        }

        # Execução do sql
        return self.fetch_one(sql, params)