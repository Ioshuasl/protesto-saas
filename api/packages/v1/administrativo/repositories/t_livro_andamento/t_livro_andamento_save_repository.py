from abstracts.repository import BaseRepository
from actions.data.generate_insert_sql import generate_insert_sql
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.t_livro_andamento_schema import TLivroAndamentoSaveSchema


class TLivroAndamentoSaveRepository(BaseRepository):
    """Repository to insert T_LIVRO_ANDAMENTO rows."""

    def execute(self, schema: TLivroAndamentoSaveSchema):
        params = schema.model_dump(exclude_unset=True)
        sql = generate_insert_sql("T_LIVRO_ANDAMENTO", params)
        return self.run_and_return(sql, params)
