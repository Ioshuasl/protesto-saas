from fastapi import HTTPException, status

from packages.v1.administrativo.actions.g_selo_livro.g_selo_livro_livre_show_action import (
    GSeloLivroLivreShowAction,
)
from packages.v1.administrativo.schemas.g_selo_livro_schema import GSeloLivroLivreSchema


class GSeloLivroLivreShowService:
    def execute(self, data: GSeloLivroLivreSchema):
        result = GSeloLivroLivreShowAction().execute(data)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao ha selos disponiveis para serem gerados",
            )

        return result
