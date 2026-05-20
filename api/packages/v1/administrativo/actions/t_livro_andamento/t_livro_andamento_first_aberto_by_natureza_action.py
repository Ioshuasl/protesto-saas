from abstracts.action import BaseAction

from packages.v1.administrativo.repositories.t_livro_andamento.t_livro_andamento_first_aberto_by_natureza_repository import (
    TLivroAndamentoFirstAbertoByNaturezaRepository,
)
from packages.v1.administrativo.schemas.t_livro_andamento_schema import (
    TLivroAndamentoNaturezaIdSchema,
)


class TLivroAndamentoFirstAbertoByNaturezaAction(BaseAction):
    """Action to get the first open T_LIVRO_ANDAMENTO row by LIVRO_NATUREZA_ID."""

    def execute(self, schema: TLivroAndamentoNaturezaIdSchema):
        return TLivroAndamentoFirstAbertoByNaturezaRepository().execute(schema)
