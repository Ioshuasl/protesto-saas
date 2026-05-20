from fastapi import HTTPException, status

from packages.v1.administrativo.actions.g_selo_livro.g_selo_livro_livre_quantidade_show_action import (
    GSeloLivroLivreQuantidadeShowAction,
)
from packages.v1.administrativo.schemas.g_selo_livro_schema import GSeloLivroLivreSchema


class GSeloLivroLivreQuantidadeShowService:
    def execute(self, data: GSeloLivroLivreSchema):
        result = GSeloLivroLivreQuantidadeShowAction().execute(data)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao ha selos disponiveis para serem gerados",
            )

        return result
