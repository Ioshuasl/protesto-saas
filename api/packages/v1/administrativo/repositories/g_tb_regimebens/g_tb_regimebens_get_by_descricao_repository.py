from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_tb_regimebens_schema import GTbRegimebensDescricaoSchema

class GetByDescricaoRepository(BaseRepository):
    """
    Repositório para a operação de busca de um registro na tabela
    g_tb_regimebens por descrição.
    """

    def execute(self, regimebens_schema: GTbRegimebensDescricaoSchema):
        """
        Executa a consulta SQL para buscar um registro pela descrição.

        Args:
            regimebens_schema (GTbRegimebensDescricaoSchema): 
                O esquema com a descrição a ser buscada.

        Returns:
            Um dicionário contendo os dados do registro ou None se não for encontrado.
        """
        # Montagem do SQL
        sql = """ SELECT * FROM G_TB_REGIMEBENS WHERE DESCRICAO = :descricao """

        # Preenchimento de parâmetros
        params = {
            'descricao': regimebens_schema.descricao
        }

        # Execução do SQL
        return self.fetch_one(sql, params)
