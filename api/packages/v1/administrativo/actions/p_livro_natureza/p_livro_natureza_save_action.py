from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_livro_natureza.p_livro_natureza_save_repository import (
    SaveRepository,
)
from packages.v1.administrativo.schemas.p_livro_natureza_schema import PLivroNaturezaSaveSchema


class SaveAction(BaseAction):
    def execute(self, livro_natureza_schema: PLivroNaturezaSaveSchema):
        return SaveRepository().execute(livro_natureza_schema)
