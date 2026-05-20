from actions.dynamic_import.dynamic_import import DynamicImport
from fastapi import HTTPException, status
from packages.v1.administrativo.actions.t_pessoa.t_pessoa_save_action import (
    TPessoaSaveAction,
)
from packages.v1.administrativo.schemas.t_pessoa_schema import (
    TPessoaCpfSchema,
    TPessoaEmailSchema,
    TPessoaSaveSchema,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService
from packages.v1.administrativo.services.t_pessoa.go.t_pessoa_get_cpf_service import (
    TPessoaGetCpfService,
)
from packages.v1.administrativo.services.t_pessoa.go.t_pessoa_get_email_service import (
    TPessoaGetEmailService,
)


class TPessoaSaveService:

    def __init__(self):
        # Ação responsável por carregar as services de acordo com o estado
        self.dynamic_import = DynamicImport()

        # Define o pacote que deve ser carregado
        self.dynamic_import.set_package("administrativo")

        # Define a tabela que o pacote pertence
        self.dynamic_import.set_table("t_pessoa")
        pass

    # Cadastra o novo regime de bens
    def execute(self, t_pessoa_save_schema: TPessoaSaveSchema):
        errors = []

        if t_pessoa_save_schema.email and str(t_pessoa_save_schema.email).strip():
            email_service = TPessoaGetEmailService()
            email_response = email_service.execute(
                TPessoaEmailSchema(email=str(t_pessoa_save_schema.email).strip()),
                False,
            )
            if email_response:
                errors.append(
                    {
                        "input": "email",
                        "message": "O e-mail informado já está sendo utilizado.",
                    }
                )

        if t_pessoa_save_schema.cpf_cnpj and str(t_pessoa_save_schema.cpf_cnpj).strip():
            cpf_service = TPessoaGetCpfService()
            cpf_response = cpf_service.execute(
                TPessoaCpfSchema(cpf=str(t_pessoa_save_schema.cpf_cnpj).strip()),
                False,
            )
            if cpf_response:
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

        # Verifica se precisa gerar o ID de sequência
        if not t_pessoa_save_schema.pessoa_id:

            # Crio um objeto de sequencia
            sequencia_schema = GSequenciaSchema()

            # Define os dados para atualizar a sequencia
            sequencia_schema.tabela = "T_PESSOA"

            # Busco a sequência atualizada
            generate = GenerateService()

            # Busco a sequência atualizada
            sequencia = generate.execute(sequencia_schema)

            # Atualiza os dados da chave primária
            t_pessoa_save_schema.pessoa_id = sequencia.sequencia

        # Instanciamento de ações
        t_pessoa_save_action = TPessoaSaveAction()

        # Retorna o resultado da operação
        return t_pessoa_save_action.execute(t_pessoa_save_schema)
