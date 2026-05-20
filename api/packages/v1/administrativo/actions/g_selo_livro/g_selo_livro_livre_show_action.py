from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_selo_livro.g_selo_livro_livre_show_repository import (
    GSeloLivroLivreIndexRepository,
)
from packages.v1.administrativo.schemas.g_selo_livro_schema import GSeloLivroLivreSchema


class GSeloLivroLivreShowAction(BaseAction):
    def execute(self, data: GSeloLivroLivreSchema):
        return GSeloLivroLivreIndexRepository().execute(data)
