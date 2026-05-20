from packages.v1.administrativo.actions.g_selo_livro.g_selo_livro_update_action import (
    GSeloLivroUpdateAction,
)
from packages.v1.administrativo.schemas.g_selo_livro_schema import GSeloLivroUpdateSchema


class GSeloLivroUpdateService:
    def execute(self, data: GSeloLivroUpdateSchema):
        return GSeloLivroUpdateAction().execute(data)
