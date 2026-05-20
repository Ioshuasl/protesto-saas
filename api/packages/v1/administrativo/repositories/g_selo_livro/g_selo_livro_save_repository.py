from abstracts.repository import BaseRepository
from actions.data.generate_insert_sql import generate_insert_sql
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.g_selo_livro_schema import GSeloLivroSaveSchema


class GSeloLivroSaveRepository(BaseRepository):
    def execute(self, data: GSeloLivroSaveSchema):
        try:
            params = data.model_dump(exclude_unset=True)
            sql = generate_insert_sql("G_SELO_LIVRO", params)

            return self.run_and_return(sql, params)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar registro em G_SELO_LIVRO: {e}",
            )
