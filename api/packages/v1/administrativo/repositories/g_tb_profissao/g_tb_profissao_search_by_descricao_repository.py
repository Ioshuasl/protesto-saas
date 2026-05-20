from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_tb_profissao_schema import GTbProfissaoDescricaoSchema


class SearchByDescricaoRepository(BaseRepository):
    """
    Repositório para a operação de busca de profissões por descrição.
    """

    def execute(self, profissao_schema: GTbProfissaoDescricaoSchema):
        """
        Executa a consulta SQL para buscar profissões por descrição.

        Args:
            profissao_schema (GTbProfissaoDescricaoSchema): O esquema com a descrição a ser buscada.

        Returns:
            Lista com as profissões localizadas.
        """
        # Montagem do SQL (busca textual por descrição)
        sql = """
            SELECT *
              FROM G_TB_PROFISSAO
             WHERE UPPER(DESCRICAO) LIKE :descricao
             ORDER BY DESCRICAO
        """

        # Preenchimento de parâmetros
        params = {
            "descricao": f"%{(profissao_schema.descricao or '').strip().upper()}%",
        }

        # Execução do SQL
        return self.fetch_all(sql, params)
