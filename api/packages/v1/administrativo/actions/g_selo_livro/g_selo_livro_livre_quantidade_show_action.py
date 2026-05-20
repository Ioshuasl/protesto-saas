from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_selo_livro.g_selo_livro_livre_show_quantidade_repository import (
    GSeloLivroLivreQuantidadeShowRepository,
)
from packages.v1.administrativo.schemas.g_selo_livro_schema import GSeloLivroLivreSchema


class GSeloLivroLivreQuantidadeShowAction(BaseAction):
    def execute(self, data: GSeloLivroLivreSchema):
        return GSeloLivroLivreQuantidadeShowRepository().execute(data)
