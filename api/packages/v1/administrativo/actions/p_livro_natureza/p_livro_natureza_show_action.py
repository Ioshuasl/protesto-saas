from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_livro_natureza.p_livro_natureza_show_repository import (
    ShowRepository,
)
from packages.v1.administrativo.schemas.p_livro_natureza_schema import PLivroNaturezaIdSchema


class ShowAction(BaseAction):
    def execute(self, livro_natureza_schema: PLivroNaturezaIdSchema):
        return ShowRepository().execute(livro_natureza_schema)
