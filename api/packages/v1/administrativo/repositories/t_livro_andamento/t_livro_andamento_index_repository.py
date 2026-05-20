from abstracts.repository import BaseRepository
from fastapi import HTTPException, status


class TLivroAndamentoIndexRepository(BaseRepository):
    """Repository to list T_LIVRO_ANDAMENTO rows."""

    def execute(self):
        sql = """
            SELECT
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
            ORDER BY TLA.LIVRO_ANDAMENTO_ID
        """
        return self.fetch_all(sql)
