from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_livro_andamento.p_livro_andamento_update_repository import (
    UpdateRepository,
)
from packages.v1.administrativo.schemas.p_livro_andamento_schema import (
    PLivroAndamentoUpdateSchema,
)


class FinalizarAction(BaseAction):
    def execute(
        self,
        livro_andamento_id: int,
        livro_andamento_schema: PLivroAndamentoUpdateSchema,
    ):
        return UpdateRepository().execute(livro_andamento_id, livro_andamento_schema)
