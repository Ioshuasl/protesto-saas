from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.g_selo_livro_schema import GSeloLivroIdSchema


class GSeloLivroShowRepository(BaseRepository):
    def execute(self, data: GSeloLivroIdSchema):
        try:
            sql = """
                SELECT
                    G.*
                FROM G_SELO_LIVRO G
                WHERE G.SELO_LIVRO_ID = :selo_livro_id
            """

            result = self.fetch_one(sql, data.model_dump(exclude_unset=True))

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Registro de G_SELO_LIVRO nao encontrado.",
                )

            return result
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao buscar registro em G_SELO_LIVRO: {e}",
            )
