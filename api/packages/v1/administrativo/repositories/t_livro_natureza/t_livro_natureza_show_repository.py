from abstracts.repository import BaseRepository

from packages.v1.administrativo.schemas.t_livro_natureza_schema import TLivroNaturezaIdSchema

class TLivroNaturezaShowRepository(BaseRepository):
    """Repositório para consultar um registro específico de T_LIVRO_NATUREZA."""

    def execute(self, schema: TLivroNaturezaIdSchema):

        sql = """
            SELECT TLN.*
            FROM T_LIVRO_NATUREZA TLN
            WHERE TLN.LIVRO_NATUREZA_ID = :livro_natureza_id
        """
        params = schema.model_dump(exclude_unset=True)

        result = self.fetch_one(sql, params)

        return result