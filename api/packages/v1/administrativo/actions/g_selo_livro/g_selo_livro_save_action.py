from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_selo_livro.g_selo_livro_save_repository import (
    GSeloLivroSaveRepository,
)
from packages.v1.administrativo.schemas.g_selo_livro_schema import GSeloLivroSaveSchema


class GSeloLivroSaveAction(BaseAction):
    def execute(self, data: GSeloLivroSaveSchema):
        return GSeloLivroSaveRepository().execute(data)
