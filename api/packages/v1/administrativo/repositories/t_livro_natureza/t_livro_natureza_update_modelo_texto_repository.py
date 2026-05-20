from abstracts.repository import BaseRepository

from packages.v1.administrativo.schemas.t_livro_natureza_schema import TLivroNaturezaUpdateModeloSchema


class TLivroNaturezaUpdateModeloTextoRepository(BaseRepository):
    """Repositório para atualizar registros em T_LIVRO_NATUREZA."""

    def execute(self, schema: TLivroNaturezaUpdateModeloSchema):

        sql = f""" UPDATE T_LIVRO_NATUREZA SET {schema.coluna} = :modelo_texto WHERE LIVRO_NATUREZA_ID = :livro_natureza_id RETURNING *;"""

        params = {
            "livro_natureza_id": schema.livro_natureza_id,
            "modelo_texto": schema.modelo_texto
        }

        response = self.run_and_return(sql, params)
        return response