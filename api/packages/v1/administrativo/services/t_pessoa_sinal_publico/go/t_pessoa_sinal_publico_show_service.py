from fastapi import HTTPException, status

from packages.v1.administrativo.actions.t_pessoa_sinal_publico.t_pessoa_sinal_publico_show_action import (
    TPessoaSinalPublicoShowAction,
)
from packages.v1.administrativo.schemas.t_pessoa_sinal_publico_schema import (
    TPessoaSinalPublicoIdSchema,
)


class TPessoaSinalPublicoShowService:
    def execute(self, pessoa_sinal_publico_schema: TPessoaSinalPublicoIdSchema):
        action = TPessoaSinalPublicoShowAction()
        data = action.execute(pessoa_sinal_publico_schema)

        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao foi possivel localizar o registro de pessoa sinal publico",
            )

        return data
