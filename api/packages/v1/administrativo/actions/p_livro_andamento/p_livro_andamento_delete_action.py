from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_livro_andamento.p_livro_andamento_delete_repository import (
    DeleteRepository,
)
from packages.v1.administrativo.schemas.p_livro_andamento_schema import PLivroAndamentoIdSchema


class DeleteAction(BaseAction):
    def execute(self, livro_andamento_schema: PLivroAndamentoIdSchema) -> bool:
        return DeleteRepository().execute(livro_andamento_schema)
