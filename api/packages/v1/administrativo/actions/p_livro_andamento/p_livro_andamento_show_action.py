from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_livro_andamento.p_livro_andamento_show_repository import (
    ShowRepository,
)
from packages.v1.administrativo.schemas.p_livro_andamento_schema import PLivroAndamentoIdSchema


class ShowAction(BaseAction):
    def execute(self, livro_andamento_schema: PLivroAndamentoIdSchema):
        return ShowRepository().execute(livro_andamento_schema)
