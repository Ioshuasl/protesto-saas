from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_selo_livro.g_selo_livro_delete_repository import (
    GSeloLivroDeleteRepository,
)
from packages.v1.administrativo.schemas.g_selo_livro_schema import GSeloLivroIdSchema


class GSeloLivroDeleteAction(BaseAction):
    def execute(self, data: GSeloLivroIdSchema):
        return GSeloLivroDeleteRepository().execute(data)
