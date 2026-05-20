from fastapi import HTTPException, status
from packages.v1.administrativo.actions.t_livro_natureza.t_livro_natureza_show_action import (
    TLivroNaturezaShowAction,
)
from packages.v1.administrativo.schemas.t_livro_natureza_schema import TLivroNaturezaIdSchema


class TLivroNaturezaShowService:
    """Servico para buscar um registro de T_LIVRO_NATUREZA."""

    def execute(self, schema: TLivroNaturezaIdSchema):

        response = TLivroNaturezaShowAction().execute(schema)

        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o registro de T_LIVRO_NATUREZA.",
            )

        return response
