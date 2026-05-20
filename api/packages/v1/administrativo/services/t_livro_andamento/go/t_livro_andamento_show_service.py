from fastapi import HTTPException, status

from packages.v1.administrativo.actions.t_livro_andamento.t_livro_andamento_show_action import (
    TLivroAndamentoShowAction,
)
from packages.v1.administrativo.schemas.t_livro_andamento_schema import TLivroAndamentoIdSchema


class TLivroAndamentoShowService:
    """Service to fetch one T_LIVRO_ANDAMENTO row."""

    def execute(self, schema: TLivroAndamentoIdSchema):
        response = TLivroAndamentoShowAction().execute(schema)

        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao foi possivel localizar o registro de T_LIVRO_ANDAMENTO.",
            )

        return response
