from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_livro_natureza.p_livro_natureza_delete_repository import (
    DeleteRepository,
)
from packages.v1.administrativo.schemas.p_livro_natureza_schema import PLivroNaturezaIdSchema


class DeleteAction(BaseAction):
    def execute(self, livro_natureza_schema: PLivroNaturezaIdSchema) -> bool:
        return DeleteRepository().execute(livro_natureza_schema)
