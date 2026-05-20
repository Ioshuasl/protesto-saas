from abstracts.repository import BaseRepository
from fastapi import HTTPException, status


class TLivroNaturezaIndexRepository(BaseRepository):
    """Repositório para listar T_LIVRO_NATUREZA."""

    def execute(self):
        try:
            sql = """
                SELECT *
                FROM T_LIVRO_NATUREZA
                ORDER BY LIVRO_NATUREZA_ID
            """
            return self.fetch_all(sql)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao listar registros de T_LIVRO_NATUREZA: {error}",
            )

