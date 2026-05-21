from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_livro_natureza.p_livro_natureza_show_action import (
    ShowAction,
)
from packages.v1.administrativo.actions.p_livro_natureza.p_livro_natureza_update_action import (
    UpdateAction,
)
from packages.v1.administrativo.schemas.p_livro_natureza_schema import (
    PLivroNaturezaIdSchema,
    PLivroNaturezaUpdateSchema,
)


class UpdateService:
    def execute(
        self, livro_natureza_id: int, livro_natureza_schema: PLivroNaturezaUpdateSchema
    ):
        current = ShowAction().execute(PLivroNaturezaIdSchema(livro_natureza_id=livro_natureza_id))
        if not current:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar a natureza de livro.",
            )

        return UpdateAction().execute(livro_natureza_id, livro_natureza_schema)
