from abstracts.action import BaseAction

from packages.v1.administrativo.repositories.t_livro_andamento.t_livro_andamento_update_repository import (
    TLivroAndamentoUpdateRepository,
)
from packages.v1.administrativo.schemas.t_livro_andamento_schema import (
    TLivroAndamentoUpdateSchema,
)


class TLivroAndamentoUpdateAction(BaseAction):
    """Action to update T_LIVRO_ANDAMENTO rows."""

    def execute(self, schema: TLivroAndamentoUpdateSchema):
        return TLivroAndamentoUpdateRepository().execute(schema)

