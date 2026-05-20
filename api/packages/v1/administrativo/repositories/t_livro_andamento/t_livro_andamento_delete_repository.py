from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.t_livro_andamento_schema import TLivroAndamentoIdSchema


class TLivroAndamentoDeleteRepository(BaseRepository):
    """Repository to delete T_LIVRO_ANDAMENTO rows."""

    def execute(self, schema: TLivroAndamentoIdSchema):
        try:
            sql = """
                DELETE FROM T_LIVRO_ANDAMENTO
                WHERE LIVRO_ANDAMENTO_ID = :livro_andamento_id
            """
            params = schema.model_dump(exclude_unset=True)
            return self.run(sql, params)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir registro de T_LIVRO_ANDAMENTO: {error}",
            )
