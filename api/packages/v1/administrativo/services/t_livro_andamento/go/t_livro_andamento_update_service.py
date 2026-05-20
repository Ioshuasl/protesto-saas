from packages.v1.administrativo.actions.t_livro_andamento.t_livro_andamento_update_action import (
    TLivroAndamentoUpdateAction,
)
from packages.v1.administrativo.schemas.t_livro_andamento_schema import (
    TLivroAndamentoUpdateSchema,
)

class TLivroAndamentoUpdateService:
    """Service to update T_LIVRO_ANDAMENTO rows."""

    def execute(self, schema: TLivroAndamentoUpdateSchema):
        return TLivroAndamentoUpdateAction().execute(schema)

