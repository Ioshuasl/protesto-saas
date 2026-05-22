from __future__ import annotations

from typing import Any

from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.p_titulo_schema import (
    PTituloIdSchema,
    _map_selo_vinculado_item,
)

_TITULO_SELOS_VINCULADOS_SQL = """
SELECT
    SO.NOTA_FISCAL,
    SL.CAMPO_ID,
    SL.NUMERO_AGRUPADOR,
    SL.NUMERO_SELO AS SIGLA,
    SL.NUMERO,
    SG.NUMERO AS TIPO_ATO,
    SG.DESCRICAO_COMPLETA,
    U.NOME_COMPLETO,
    SL.DATA,
    SL.DESCRICAO,
    SL.VALOR_TOTAL,
    SL.VALOR_EMOLUMENTO,
    SL.VALOR_TAXA_JUDICIARIA,
    SL.VALOR_FUNDESP,
    SL.SELO_LIVRO_ID
FROM G_SELO_LIVRO SL
LEFT JOIN G_SELO_LOTE SO ON SL.SELO_LOTE_ID = SO.SELO_LOTE_ID
LEFT JOIN G_SELO_GRUPO SG ON SO.SELO_GRUPO_ID = SG.SELO_GRUPO_ID
LEFT JOIN G_USUARIO U ON SL.USUARIO_ID = U.USUARIO_ID
WHERE SL.CAMPO_ID = :titulo_id
  AND SL.TABELA = 'P_TITULO'

UNION ALL

SELECT
    SO.NOTA_FISCAL,
    SL.CAMPO_ID,
    SL.NUMERO_AGRUPADOR,
    SL.SIGLA || LPAD(CAST(SL.NUMERO AS INTEGER), 5, '0') AS SIGLA,
    SL.NUMERO,
    SG.NUMERO AS TIPO_ATO,
    SG.DESCRICAO_COMPLETA,
    U.NOME_COMPLETO,
    SL.DATA,
    SL.DESCRICAO,
    SL.VALOR_TOTAL,
    SL.VALOR_EMOLUMENTO,
    SL.VALOR_TAXA_JUDICIARIA,
    SL.VALOR_FUNDESP,
    SL.SELO_LIVRO_ID
FROM G_SELO_LIVRO_ANTIGO SL
LEFT JOIN G_SELO_LOTE_ANTIGO SO ON SL.SELO_LOTE_ID = SO.SELO_LOTE_ID
LEFT JOIN G_SELO_GRUPO SG ON SO.SELO_GRUPO_ID = SG.SELO_GRUPO_ID
LEFT JOIN G_USUARIO U ON SL.USUARIO_ID = U.USUARIO_ID
WHERE SL.CAMPO_ID = :titulo_id
  AND UPPER(SL.TABELA) = 'P_TITULO'
ORDER BY 14
"""


class SelosRepository(BaseRepository):
    def execute(self, titulo_schema: PTituloIdSchema) -> list[dict[str, Any]]:
        titulo_id = titulo_schema.titulo_id
        rows = self.fetch_all(_TITULO_SELOS_VINCULADOS_SQL, {"titulo_id": titulo_id})
        return [_map_selo_vinculado_item(row) for row in rows if row is not None]

    def titulo_exists(self, titulo_id: int) -> bool:
        row = self.fetch_one(
            """
            SELECT TITULO_ID
            FROM P_TITULO
            WHERE TITULO_ID = :titulo_id
            """,
            {"titulo_id": titulo_id},
        )
        return row is not None
