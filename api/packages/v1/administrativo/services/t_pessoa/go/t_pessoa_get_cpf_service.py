from fastapi import HTTPException, status

from packages.v1.administrativo.actions.t_pessoa.t_pessoa_get_by_cpf_action import (
    TPessoaGetByCpfAction,
)
from packages.v1.administrativo.schemas.t_pessoa_schema import TPessoaCpfSchema


class TPessoaGetCpfService:
    def execute(self, t_pessoa_cpf_schema: TPessoaCpfSchema, messageValidate: bool = True):
        action = TPessoaGetByCpfAction()
        data = action.execute(t_pessoa_cpf_schema)

        if messageValidate and not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao foi possivel localizar pessoa com o CPF informado",
            )

        return data
