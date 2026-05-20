from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.g_selo_livro_schema import GSeloLivroLivreSchema


class GSeloLivroLivreIndexRepository(BaseRepository):
    def execute(self, data: GSeloLivroLivreSchema):
        try:
            sql = """
                SELECT
                    FIRST 1 GSLV.*
                FROM
                    G_SELO_LIVRO GSLV
                JOIN G_SELO_LOTE GSLT
                    ON GSLV.SELO_LOTE_ID = GSLT.SELO_LOTE_ID
                JOIN G_SELO_GRUPO GSG
                    ON GSLT.SELO_GRUPO_ID = GSG.SELO_GRUPO_ID
                JOIN G_EMOLUMENTO_ITEM GEI
                    ON GSG.SELO_GRUPO_ID = GEI.SELO_GRUPO_ID
                WHERE
                    GEI.SELO_GRUPO_ID = :selo_grupo_id
                    AND GSLV.SELO_SITUACAO_ID = 1
                    AND GSLT.SITUACAO = 'I'
                ORDER BY
                    GSLV.SELO_LIVRO_ID;
            """

            return self.fetch_one(sql, data.model_dump(exclude_unset=True))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao listar registros de G_SELO_LIVRO: {e}",
            )
