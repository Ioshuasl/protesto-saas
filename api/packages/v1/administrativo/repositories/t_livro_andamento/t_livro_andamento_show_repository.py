from abstracts.repository import BaseRepository

from packages.v1.administrativo.schemas.t_livro_andamento_schema import TLivroAndamentoIdSchema


class TLivroAndamentoShowRepository(BaseRepository):
    """Repository to fetch one T_LIVRO_ANDAMENTO row."""

    def execute(self, schema: TLivroAndamentoIdSchema):
        sql = """
            SELECT TLA.*
            FROM T_LIVRO_ANDAMENTO TLA
            WHERE TLA.LIVRO_ANDAMENTO_ID = :livro_andamento_id
        """
        params = schema.model_dump(exclude_unset=True)
        return self.fetch_one(sql, params)
