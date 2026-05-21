from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_livro_natureza.p_livro_natureza_show_action import (
    ShowAction,
)
from packages.v1.administrativo.schemas.p_livro_natureza_schema import PLivroNaturezaIdSchema


class ShowService:
    def execute(self, livro_natureza_schema: PLivroNaturezaIdSchema):
        data = ShowAction().execute(livro_natureza_schema)

        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar a natureza de livro.",
            )

        return data
