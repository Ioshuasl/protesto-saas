from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_livro_andamento.p_livro_andamento_max_numero_livro_repository import (
    MaxNumeroLivroRepository,
)
from packages.v1.administrativo.schemas.p_livro_andamento_schema import (
    PLivroAndamentoNaturezaIdSchema,
)


class MaxNumeroLivroAction(BaseAction):
    def execute(self, schema: PLivroAndamentoNaturezaIdSchema) -> dict[str, int]:
        return MaxNumeroLivroRepository().execute(schema)
