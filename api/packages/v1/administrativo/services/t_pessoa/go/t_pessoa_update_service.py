from fastapi import HTTPException, status
from packages.v1.administrativo.actions.t_pessoa.t_pessoa_update_action import (
    TPessoaUpdateAction,
)
from packages.v1.administrativo.schemas.t_pessoa_schema import (
    TPessoaCpfSchema,
    TPessoaEmailSchema,
    TPessoaUpdateSchema,
)
from packages.v1.administrativo.services.t_pessoa.go.t_pessoa_get_cpf_service import (
    TPessoaGetCpfService,
)
from packages.v1.administrativo.services.t_pessoa.go.t_pessoa_get_email_service import (
    TPessoaGetEmailService,
)


class TPessoaUpdateService:
    """
    Serviço para a operação de atualização de um registro na tabela
    g_tb_regimebens.
    """

    def execute(self, t_pessoa_update_schema: TPessoaUpdateSchema):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            regimebens_schema (GTbRegimebensUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        errors = []

        if t_pessoa_update_schema.email and str(t_pessoa_update_schema.email).strip():
            email_service = TPessoaGetEmailService()
            email_response = email_service.execute(
                TPessoaEmailSchema(email=str(t_pessoa_update_schema.email).strip()),
                False,
            )
            if (
                email_response
                and email_response.get("pessoa_id")
                and int(float(email_response.get("pessoa_id"))) != t_pessoa_update_schema.pessoa_id
            ):
                errors.append(
                    {
                        "input": "email",
                        "message": "O e-mail informado já está sendo utilizado.",
                    }
                )

        if t_pessoa_update_schema.cpf_cnpj and str(t_pessoa_update_schema.cpf_cnpj).strip():
            cpf_service = TPessoaGetCpfService()
            cpf_response = cpf_service.execute(
                TPessoaCpfSchema(cpf=str(t_pessoa_update_schema.cpf_cnpj).strip()),
                False,
            )
            if (
                cpf_response
                and cpf_response.get("pessoa_id")
                and int(float(cpf_response.get("pessoa_id"))) != t_pessoa_update_schema.pessoa_id
            ):
                errors.append(
                    {
                        "input": "cpf_cnpj",
                        "message": "O CPF informado já está sendo utilizado.",
                    }
                )

        if errors:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=errors,
            )

        # Instanciamento de ações
        t_pessoa_update_action = TPessoaUpdateAction()

        # Retorna o resultado da operação
        return t_pessoa_update_action.execute(t_pessoa_update_schema)
