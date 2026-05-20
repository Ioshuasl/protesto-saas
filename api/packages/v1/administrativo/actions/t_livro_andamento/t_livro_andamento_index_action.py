from abstracts.action import BaseAction

from packages.v1.administrativo.repositories.t_livro_andamento.t_livro_andamento_index_repository import (
    TLivroAndamentoIndexRepository,
)


class TLivroAndamentoIndexAction(BaseAction):
    """Action to list T_LIVRO_ANDAMENTO rows."""

    def execute(self):
        return TLivroAndamentoIndexRepository().execute()
