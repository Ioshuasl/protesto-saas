from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_livro_andamento.p_livro_andamento_show_action import (
    ShowAction,
)
from packages.v1.administrativo.schemas.p_livro_andamento_schema import PLivroAndamentoIdSchema


class ShowService:
    def execute(self, livro_andamento_schema: PLivroAndamentoIdSchema):
        data = ShowAction().execute(livro_andamento_schema)

        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o livro de andamento.",
            )

        return data
