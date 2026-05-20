from packages.v1.administrativo.actions.t_livro_andamento.t_livro_andamento_first_aberto_by_natureza_action import (
    TLivroAndamentoFirstAbertoByNaturezaAction,
)
from packages.v1.administrativo.schemas.t_livro_andamento_schema import (
    TLivroAndamentoNaturezaIdSchema,
)


class TLivroAndamentoFirstAbertoByNaturezaService:
    """Service to get the first open T_LIVRO_ANDAMENTO row by LIVRO_NATUREZA_ID."""

    def execute(self, schema: TLivroAndamentoNaturezaIdSchema):
        return TLivroAndamentoFirstAbertoByNaturezaAction().execute(schema)
