from abstracts.action import BaseAction

from packages.v1.administrativo.repositories.t_livro_andamento.t_livro_andamento_save_repository import (
    TLivroAndamentoSaveRepository,
)
from packages.v1.administrativo.schemas.t_livro_andamento_schema import TLivroAndamentoSaveSchema


class TLivroAndamentoSaveAction(BaseAction):
    """Action to insert one T_LIVRO_ANDAMENTO row."""

    def execute(self, schema: TLivroAndamentoSaveSchema):
        return TLivroAndamentoSaveRepository().execute(schema)
