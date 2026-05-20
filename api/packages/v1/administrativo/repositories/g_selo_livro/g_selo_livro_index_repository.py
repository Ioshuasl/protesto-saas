from abstracts.repository import BaseRepository
from fastapi import HTTPException, status


class GSeloLivroIndexRepository(BaseRepository):
    def execute(self):
        try:
            sql = """
                SELECT FIRST 1000
                    G.*
                FROM G_SELO_LIVRO G
            """

            return self.fetch_all(sql)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao listar registros de G_SELO_LIVRO: {e}",
            )
