from abstracts.action import BaseAction

from packages.v1.administrativo.repositories.t_livro_natureza.t_livro_natureza_delete_repository import (
    TLivroNaturezaDeleteRepository,
)
from packages.v1.administrativo.schemas.t_livro_natureza_schema import TLivroNaturezaIdSchema


class TLivroNaturezaDeleteAction(BaseAction):
    """Action para excluir um registro de T_LIVRO_NATUREZA."""

    def execute(self, schema: TLivroNaturezaIdSchema):
        repository = TLivroNaturezaDeleteRepository()
        return repository.execute(schema)
