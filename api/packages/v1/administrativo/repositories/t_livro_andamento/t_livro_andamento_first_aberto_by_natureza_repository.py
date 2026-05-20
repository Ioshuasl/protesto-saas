from abstracts.repository import BaseRepository

from packages.v1.administrativo.schemas.t_livro_andamento_schema import (
    TLivroAndamentoNaturezaIdSchema,
)


class TLivroAndamentoFirstAbertoByNaturezaRepository(BaseRepository):
    """Repository to get the first open T_LIVRO_ANDAMENTO row by LIVRO_NATUREZA_ID."""

    def execute(self, schema: TLivroAndamentoNaturezaIdSchema):
        sql = """
            SELECT FIRST 1
                TLA.LIVRO_ANDAMENTO_ID,
                TLA.LIVRO_NATUREZA_ID,
                TLN.DESCRICAO,
                TLA.FOLHA_ATUAL,
                TLA.NUMERO_LIVRO,
                TLA.NUMERO_LIVRO_LETRA,
                TLA.DATA_ABERTURA,
                TLA.DATA_FECHAMENTO,
                TLA.NUMERO_FOLHAS,
                TLA.ANTIGO,
                TLA.C_ATO_FRENTEVERSO_ATUAL,
                TLA.CHAVE_IMPORTACAO
            FROM T_LIVRO_ANDAMENTO TLA
            LEFT JOIN T_LIVRO_NATUREZA TLN ON TLA.LIVRO_NATUREZA_ID = TLN.LIVRO_NATUREZA_ID
            WHERE TLA.LIVRO_NATUREZA_ID = :livro_natureza_id
              AND TLA.DATA_ABERTURA IS NOT NULL
              AND COALESCE(TLA.ANTIGO, 'N') <> 'S'
            ORDER BY TLA.LIVRO_ANDAMENTO_ID
        """

        params = {"livro_natureza_id": schema.livro_natureza_id}
        return self.fetch_one(sql, params)
