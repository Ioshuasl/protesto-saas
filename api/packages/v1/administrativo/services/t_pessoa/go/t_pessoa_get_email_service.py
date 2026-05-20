from fastapi import HTTPException, status

from packages.v1.administrativo.actions.t_pessoa.t_pessoa_get_by_email_action import (
    TPessoaGetByEmailAction,
)
from packages.v1.administrativo.schemas.t_pessoa_schema import TPessoaEmailSchema


class TPessoaGetEmailService:
    def execute(self, t_pessoa_email_schema: TPessoaEmailSchema, messageValidate: bool = True):
        action = TPessoaGetByEmailAction()
        data = action.execute(t_pessoa_email_schema)

        if messageValidate and not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao foi possivel localizar pessoa com o e-mail informado",
            )

        return data
