from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_livro_andamento.p_livro_andamento_save_repository import (
    SaveRepository,
)
from packages.v1.administrativo.schemas.p_livro_andamento_schema import PLivroAndamentoSaveSchema


class SaveAction(BaseAction):
    def execute(self, livro_andamento_schema: PLivroAndamentoSaveSchema):
        return SaveRepository().execute(livro_andamento_schema)
