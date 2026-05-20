from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.t_livro_natureza_schema import TLivroNaturezaIdSchema


class TLivroNaturezaDeleteRepository(BaseRepository):
    """Repositório para excluir registros em T_LIVRO_NATUREZA."""

    def execute(self, schema: TLivroNaturezaIdSchema):
        try:
            sql = """
                DELETE FROM T_LIVRO_NATUREZA
                WHERE LIVRO_NATUREZA_ID = :livro_natureza_id
            """
            params = schema.model_dump(exclude_unset=True)
            return self.run(sql, params)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir registro de T_LIVRO_NATUREZA: {error}",
            )
