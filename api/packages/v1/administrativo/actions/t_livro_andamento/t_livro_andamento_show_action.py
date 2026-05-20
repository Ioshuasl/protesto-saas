from abstracts.action import BaseAction

from packages.v1.administrativo.repositories.t_livro_andamento.t_livro_andamento_show_repository import (
    TLivroAndamentoShowRepository,
)
from packages.v1.administrativo.schemas.t_livro_andamento_schema import TLivroAndamentoIdSchema


class TLivroAndamentoShowAction(BaseAction):
    """Action to fetch one T_LIVRO_ANDAMENTO row."""

    def execute(self, schema: TLivroAndamentoIdSchema):
        return TLivroAndamentoShowRepository().execute(schema)
