from abstracts.action import BaseAction

from packages.v1.administrativo.repositories.t_livro_natureza.t_livro_natureza_save_repository import (
    TLivroNaturezaSaveRepository,
)
from packages.v1.administrativo.schemas.t_livro_natureza_schema import TLivroNaturezaSaveSchema


class TLivroNaturezaSaveAction(BaseAction):
    """Action para salvar um registro em T_LIVRO_NATUREZA."""

    def execute(self, schema: TLivroNaturezaSaveSchema):
        repository = TLivroNaturezaSaveRepository()
        return repository.execute(schema)
