from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.g_selo_livro_schema import GSeloLivroIdSchema


class GSeloLivroDeleteRepository(BaseRepository):
    def execute(self, data: GSeloLivroIdSchema):
        try:
            sql = """
                DELETE FROM G_SELO_LIVRO
                WHERE SELO_LIVRO_ID = :selo_livro_id
                RETURNING SELO_LIVRO_ID
            """

            params = {"selo_livro_id": data.selo_livro_id}
            return self.run_and_return(sql, params)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir registro de G_SELO_LIVRO: {e}",
            )
