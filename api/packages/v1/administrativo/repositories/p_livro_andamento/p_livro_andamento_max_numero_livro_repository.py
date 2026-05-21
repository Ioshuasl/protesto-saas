from __future__ import annotations

from decimal import Decimal

from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.p_livro_andamento_schema import (
    PLivroAndamentoNaturezaIdSchema,
)


class MaxNumeroLivroRepository(BaseRepository):
    """Maior NUMERO_LIVRO por LIVRO_NATUREZA_ID (sugestão = max + 1)."""

    def execute(self, schema: PLivroAndamentoNaturezaIdSchema) -> dict[str, int]:
        sql = """
        SELECT MAX(NUMERO_LIVRO) AS MAX_NUMERO
        FROM P_LIVRO_ANDAMENTO
        WHERE LIVRO_NATUREZA_ID = :livro_natureza_id
        """
        row = self.fetch_one(
            sql, {"livro_natureza_id": schema.livro_natureza_id}
        ) or {}
        max_numero = row.get("MAX_NUMERO") or row.get("max_numero")
        if isinstance(max_numero, Decimal):
            max_numero = int(max_numero)
        max_val = int(max_numero or 0)
        return {
            "livro_natureza_id": schema.livro_natureza_id,
            "max_numero_livro": max_val,
            "numero_livro_sugerido": max_val + 1,
        }
