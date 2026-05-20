from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_selo_livro_schema import GSeloLivroSchema


class GSeloLivroShowByTabelaCampoRepository(BaseRepository):

    def execute(self, data: GSeloLivroSchema):
        sql = """
            SELECT
                FIRST 1
                GSL.SELO_LIVRO_ID,
                GSL.NUMERO_AGRUPADOR,
                GSL.NUMERO_SELO,
                GSL.TABELA,
                GSL.CAMPO_ID
            FROM
                G_SELO_LIVRO GSL
            WHERE
                GSL.TABELA = :tabela
                AND GSL.CAMPO_ID = :campo_id
            ORDER BY
                GSL.SELO_LIVRO_ID DESC
        """

        params = {
            "tabela": data.tabela,
            "campo_id": data.campo_id,
        }

        return self.fetch_one(sql, params)
