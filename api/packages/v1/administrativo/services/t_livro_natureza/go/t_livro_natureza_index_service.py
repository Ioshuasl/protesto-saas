from packages.v1.administrativo.actions.t_livro_natureza.t_livro_natureza_index_action import (
    TLivroNaturezaIndexAction,
)


class TLivroNaturezaIndexService:
    """Servico para listar T_LIVRO_NATUREZA."""

    def execute(self):
        action = TLivroNaturezaIndexAction()
        return action.execute()
