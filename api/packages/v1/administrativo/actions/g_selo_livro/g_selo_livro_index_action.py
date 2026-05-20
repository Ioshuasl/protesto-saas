from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_selo_livro.g_selo_livro_index_repository import (
    GSeloLivroIndexRepository,
)


class GSeloLivroIndexAction(BaseAction):
    def execute(self):
        return GSeloLivroIndexRepository().execute()
