from abstracts.action import BaseAction

from packages.v1.administrativo.repositories.t_livro_natureza.t_livro_natureza_update_repository import (
    TLivroNaturezaUpdateRepository,
)
from packages.v1.administrativo.schemas.t_livro_natureza_schema import TLivroNaturezaUpdateSchema


class TLivroNaturezaUpdateAction(BaseAction):
    """Action para atualizar um registro em T_LIVRO_NATUREZA."""

    def execute(self, schema: TLivroNaturezaUpdateSchema):
        repository = TLivroNaturezaUpdateRepository()
        return repository.execute(schema)
