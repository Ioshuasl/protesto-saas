from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_tb_tipologradouro_schema import GTbTipoLogradouroDescricaoSchema

class GetByDescricaoRepository(BaseRepository):
    """
    Repositório para a operação de busca de um registro na tabela
    g_tb_tipologradouro por descricao.
    """

    def execute(self, tipologradouro_schema: GTbTipoLogradouroDescricaoSchema):
        """
        Executa a consulta SQL para buscar um registro pela descricao.

        Args:
            tipologradouro_schema (GTbTipoLogradouroDescricaoSchema): O esquema com a descricao a ser buscada.

        Returns:
            Um dicionário contendo os dados do registro ou None se não for encontrado.
        """
        # Montagem do SQL
        sql = """ SELECT * FROM G_TB_TIPOLOGRADOURO WHERE DESCRICAO = :descricao """

        # Preenchimento de parâmetros
        params = {
            'descricao': tipologradouro_schema.descricao
        }

        # Execução do sql
        return self.fetch_one(sql, params)