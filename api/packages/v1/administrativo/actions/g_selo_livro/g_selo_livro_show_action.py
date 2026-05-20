from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_selo_livro.g_selo_livro_show_repository import (
    GSeloLivroShowRepository,
)
from packages.v1.administrativo.schemas.g_selo_livro_schema import GSeloLivroIdSchema


class GSeloLivroShowAction(BaseAction):
    def execute(self, data: GSeloLivroIdSchema):
        return GSeloLivroShowRepository().execute(data)
