from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.g_selo_livro_schema import GSeloLivroLivreSchema


class GSeloLivroLivreQuantidadeShowRepository(BaseRepository):
    def execute(self, data: GSeloLivroLivreSchema):
        try:
            sql = """
                SELECT
                    GSLT.QUANTIDADE AS quantidade_total,
                    COUNT(GSL.SELO_LIVRO_ID) AS quantidade_livre,
                    GSLT.NOTA_FISCAL,
                    GSG.DESCRICAO_COMPLETA
                FROM
                    G_SELO_LIVRO GSL
                JOIN G_SELO_LOTE GSLT
                    ON GSL.SELO_LOTE_ID = GSLT.SELO_LOTE_ID
                JOIN G_SELO_GRUPO GSG
                    ON GSG.SELO_GRUPO_ID = GSLT.SELO_GRUPO_ID
                WHERE
                    GSLT.SITUACAO = :situacao
                    AND GSL.SELO_SITUACAO_ID = :selo_situacao_id
                    AND GSG.SELO_GRUPO_ID = :selo_grupo_id
                GROUP BY
                    GSLT.QUANTIDADE,
                    GSLT.NOTA_FISCAL,
                    GSG.DESCRICAO_COMPLETA;
            """
            params = {
                "situacao": "I",
                "selo_situacao_id": 1,
                "selo_grupo_id": data.selo_grupo_id,
            }

            return self.fetch_one(sql, params)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao listar registros de G_SELO_LIVRO: {e}",
            )
