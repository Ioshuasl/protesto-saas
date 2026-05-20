from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_selo_livro.g_selo_livro_update_repository import (
    GSeloLivroUpdateRepository,
)
from packages.v1.administrativo.schemas.g_selo_livro_schema import GSeloLivroUpdateSchema


class GSeloLivroUpdateAction(BaseAction):
    def execute(self, data: GSeloLivroUpdateSchema):
        return GSeloLivroUpdateRepository().execute(data)
