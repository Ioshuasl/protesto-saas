from abstracts.action import BaseAction

from packages.v1.administrativo.repositories.t_livro_natureza.t_livro_natureza_index_repository import (
    TLivroNaturezaIndexRepository,
)


class TLivroNaturezaIndexAction(BaseAction):
    """Action para indexar registros de T_LIVRO_NATUREZA."""

    def execute(self):
        repository = TLivroNaturezaIndexRepository()
        return repository.execute()
