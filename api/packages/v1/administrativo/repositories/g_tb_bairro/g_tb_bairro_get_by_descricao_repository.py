from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_tb_bairro_schema import GTbBairroDescricaoSchema

class GetByDescricaoRepository(BaseRepository):
    """
    Repositório para a operação de busca de um registro na tabela
    g_tb_bairro por descrição.
    """

    def execute(self, bairro_schema: GTbBairroDescricaoSchema):
        """
        Executa a consulta SQL para buscar um registro pela descrição.

        Args:
            bairro_schema (GTbBairroDescricaoSchema): O esquema com a descrição a ser buscada.

        Returns:
            Um dicionário contendo os dados do registro ou None se não for encontrado.
        """
        # Montagem do SQL
        sql = """ SELECT * FROM G_TB_BAIRRO WHERE DESCRICAO = :descricao """

        # Preenchimento de parâmetros
        params = {
            'descricao': bairro_schema.descricao
        }

        # Execução do sql
        return self.fetch_one(sql, params)