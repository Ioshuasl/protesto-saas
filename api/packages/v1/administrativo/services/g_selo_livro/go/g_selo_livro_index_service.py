from fastapi import HTTPException, status

from packages.v1.administrativo.actions.g_selo_livro.g_selo_livro_index_action import (
    GSeloLivroIndexAction,
)


class GSeloLivroIndexService:
    def execute(self):
        data = GSeloLivroIndexAction().execute()

        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao foi possivel localizar registros de G_SELO_LIVRO.",
            )

        return data
