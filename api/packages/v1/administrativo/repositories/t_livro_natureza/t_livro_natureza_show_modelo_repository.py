from abstracts.repository import BaseRepository

from packages.v1.administrativo.schemas.t_livro_natureza_schema import TLivroNaturezaShowModeloSchema

class TLivroNaturezaShowModeloRepository(BaseRepository):

    """Repositório para consultar um registro específico de T_LIVRO_NATUREZA."""

    def execute(self, schema: TLivroNaturezaShowModeloSchema):

        sql = f""" SELECT TLN.livro_natureza_id, TLN.{schema.coluna} AS MODELO_TEXTO FROM T_LIVRO_NATUREZA TLN WHERE TLN.LIVRO_NATUREZA_ID = :livro_natureza_id """

        params = {
            "livro_natureza_id": schema.livro_natureza_id
        }

        result = self.fetch_one(sql, params)

        return result