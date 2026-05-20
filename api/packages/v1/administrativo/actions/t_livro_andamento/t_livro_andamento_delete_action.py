from abstracts.action import BaseAction

from packages.v1.administrativo.repositories.t_livro_andamento.t_livro_andamento_delete_repository import (
    TLivroAndamentoDeleteRepository,
)
from packages.v1.administrativo.schemas.t_livro_andamento_schema import TLivroAndamentoIdSchema


class TLivroAndamentoDeleteAction(BaseAction):
    """Action to delete one T_LIVRO_ANDAMENTO row."""

    def execute(self, schema: TLivroAndamentoIdSchema):
        return TLivroAndamentoDeleteRepository().execute(schema)
