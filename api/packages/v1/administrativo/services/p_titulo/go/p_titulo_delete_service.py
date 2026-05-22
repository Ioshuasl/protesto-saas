from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_titulo.p_titulo_delete_action import (
    DeleteAction,
)
from packages.v1.administrativo.actions.p_titulo.p_titulo_show_action import ShowAction
from packages.v1.administrativo.repositories.p_titulo.p_titulo_count_dependents_repository import (
    CountDependentsRepository,
)
from packages.v1.administrativo.schemas.p_titulo_schema import PTituloIdSchema


class DeleteService:
    def execute(self, titulo_schema: PTituloIdSchema):
        row = ShowAction().execute(titulo_schema)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Título não encontrado.",
            )

        dependents = CountDependentsRepository().execute(titulo_schema)
        if dependents["pessoa_vinculos"] > 0 or dependents["andamentos"] > 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=[
                    {
                        "input": "titulo_id",
                        "message": (
                            "Não é possível excluir o título: existem vínculos de "
                            "pessoa ou andamentos associados."
                        ),
                    }
                ],
            )

        return DeleteAction().execute(titulo_schema)
