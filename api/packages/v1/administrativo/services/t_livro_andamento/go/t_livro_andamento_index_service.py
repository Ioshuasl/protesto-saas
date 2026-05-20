from packages.v1.administrativo.actions.t_livro_andamento.t_livro_andamento_index_action import (
    TLivroAndamentoIndexAction,
)


class TLivroAndamentoIndexService:
    """Service to list T_LIVRO_ANDAMENTO rows."""

    def execute(self):
        return TLivroAndamentoIndexAction().execute()
