from typing import Optional

from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_gramatica_schema import GGramaticaPalavraSchema


class GGramaticaGetByPalavraRepository(BaseRepository):
    def execute(self, g_gramatica_palavra_schema: GGramaticaPalavraSchema) -> Optional[dict]:
        sql = """
            SELECT
                GG.PALAVRA,
                GG.PREFIXO,
                GG.SUFIXO_MS,
                GG.SUFIXO_MP,
                GG.SUFIXO_FS,
                GG.SUFIXO_FP
            FROM G_GRAMATICA GG
            WHERE UPPER(TRIM(GG.PALAVRA)) like UPPER(TRIM(:palavra))
            ORDER BY
                CASE
                    WHEN
                        TRIM(COALESCE(GG.PREFIXO, '')) <> ''
                        OR TRIM(COALESCE(GG.SUFIXO_MS, '')) <> ''
                        OR TRIM(COALESCE(GG.SUFIXO_MP, '')) <> ''
                        OR TRIM(COALESCE(GG.SUFIXO_FS, '')) <> ''
                        OR TRIM(COALESCE(GG.SUFIXO_FP, '')) <> ''
                    THEN 0
                    ELSE 1
                END,
                GG.GRAMATICA_ID DESC
            ROWS 1
        """

        params = {
            "palavra": str(g_gramatica_palavra_schema.palavra or "").strip().upper(),
        }
        return self.fetch_one(sql, params)
