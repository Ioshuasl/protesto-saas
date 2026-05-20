from fastapi import HTTPException, status

from packages.v1.administrativo.actions.t_pessoa_sinal_publico.t_pessoa_sinal_publico_index_action import (
    TPessoaSinalPublicoIndexAction,
)
from packages.v1.administrativo.schemas.t_pessoa_sinal_publico_schema import (
    TPessoaSinalPublicoSchema,
)


class TPessoaSinalPublicoIndexService:
    def execute(self, data: TPessoaSinalPublicoSchema):
        action = TPessoaSinalPublicoIndexAction()
        data = action.execute(data)

        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao foi possivel localizar os registros de pessoa sinal publico",
            )

        return data
