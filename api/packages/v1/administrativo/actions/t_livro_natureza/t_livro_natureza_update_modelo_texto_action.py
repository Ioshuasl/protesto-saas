from abstracts.action import BaseAction

from packages.v1.administrativo.repositories.t_livro_natureza.t_livro_natureza_update_modelo_texto_repository import TLivroNaturezaUpdateModeloTextoRepository
from packages.v1.administrativo.schemas.t_livro_natureza_schema import TLivroNaturezaUpdateModeloSchema


class TLivroNaturezaUpdateModeloTextoAction(BaseAction):
    """Action para atualizar um registro em T_LIVRO_NATUREZA."""

    def execute(self, schema: TLivroNaturezaUpdateModeloSchema):
        return TLivroNaturezaUpdateModeloTextoRepository().execute(schema)

