from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_tb_profissao_schema import GTbProfissaoDescricaoSchema

class GetByDescricaoRepository(BaseRepository):
    """
    Repositório para a operação de busca de um registro na tabela
    G_TB_PROFISSAO por descrição.
    """

    def execute(self, profissao_schema: GTbProfissaoDescricaoSchema):
        """
        Executa a consulta SQL para buscar um registro pela descrição.

        Args:
            profissao_schema (GTbProfissaoDescricaoSchema): O esquema com a descrição a ser buscada.

        Returns:
            Um dicionário contendo os dados do registro ou None se não for encontrado.
        """
        # Montagem do SQL
        sql = """ SELECT * FROM G_TB_PROFISSAO WHERE DESCRICAO = :descricao """

        # Preenchimento de parâmetros
        params = {
            'descricao': profissao_schema.descricao
        }

        # Execução do sql
        return self.fetch_one(sql, params)