from abstracts.action import BaseAction

from packages.v1.administrativo.repositories.t_livro_natureza.t_livro_natureza_show_repository import (
    TLivroNaturezaShowRepository,
)
from packages.v1.administrativo.schemas.t_livro_natureza_schema import TLivroNaturezaIdSchema, TLivroNaturezaShowModeloSchema


class TLivroNaturezaShowAction(BaseAction):
    """Action para buscar um registro específico de T_LIVRO_NATUREZA."""

    def execute(self, schema: TLivroNaturezaShowModeloSchema):
        repository = TLivroNaturezaShowRepository()
        return repository.execute(schema)

