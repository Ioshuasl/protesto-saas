from abstracts.repository import BaseRepository
from actions.data.generate_insert_sql import generate_insert_sql
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.t_livro_natureza_schema import TLivroNaturezaSaveSchema


class TLivroNaturezaSaveRepository(BaseRepository):
    """Repositório para criar registros em T_LIVRO_NATUREZA."""

    def execute(self, schema: TLivroNaturezaSaveSchema):
        try:
            params = schema.model_dump(exclude_unset=True)
            sql = generate_insert_sql("T_LIVRO_NATUREZA", params)
            return self.run_and_return(sql, params)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar registro em T_LIVRO_NATUREZA: {error}",
            )
