from fastapi import HTTPException, status

from packages.v1.administrativo.actions.g_selo_livro.g_selo_livro_show_action import (
    GSeloLivroShowAction,
)
from packages.v1.administrativo.schemas.g_selo_livro_schema import GSeloLivroIdSchema


class GSeloLivroShowService:
    def execute(self, data: GSeloLivroIdSchema):
        result = GSeloLivroShowAction().execute(data)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao foi possivel localizar o registro de G_SELO_LIVRO.",
            )

        return result
