from packages.v1.administrativo.schemas.t_pessoa_schema import (
    TPessoaCpfSchema,
    TPessoaEmailSchema,
    TPessoaIdSchema,
    TPessoaNameSchema,
    TPessoaSaveFotoSchema,
    TPessoaSaveSchema,
    TPessoaTipoSchema,
    TPessoaUpdateSchema,
)
from packages.v1.administrativo.services.t_pessoa.go.t_pessoa_delete_service import (
    TPessoaDeleteService,
)
from packages.v1.administrativo.services.t_pessoa.go.t_pessoa_files_index_service import (
    TPessoaFilesIndexService,
)
from packages.v1.administrativo.services.t_pessoa.go.t_pessoa_get_cpf_service import (
    TPessoaGetCpfService,
)
from packages.v1.administrativo.services.t_pessoa.go.t_pessoa_get_email_service import (
    TPessoaGetEmailService,
)
from packages.v1.administrativo.services.t_pessoa.go.t_pessoa_index_service import (
    TPessoaIndexService,
)
from packages.v1.administrativo.services.t_pessoa.go.t_pessoa_save_foto_service import (
    TPessoaSaveFotoService,
)
from packages.v1.administrativo.services.t_pessoa.go.t_pessoa_save_service import (
    TPessoaSaveService,
)
from packages.v1.administrativo.services.t_pessoa.go.t_pessoa_show_service import (
    TPessoaShowService,
)
from packages.v1.administrativo.services.t_pessoa.go.t_pessoa_update_service import (
    TPessoaUpdateService,
)


class TPessoaController:

    def __init__(self):
        pass

    # Lista pessoas de acordo com o tipo informado
    def index(self, data: TPessoaTipoSchema):

        # Retorna lista de pessoas filtradas pelo tipo
        return {
            "message": "Pessoas localizados com sucesso",
            "data": TPessoaIndexService().execute(data),
        }

    # Lista pessoas de acordo com o tipo informado
    def files_index(self, data: TPessoaIdSchema):

        # Retorna lista de pessoas filtradas pelo tipo
        return {
            "message": "Pessoas localizados com sucesso",
            "data": TPessoaFilesIndexService().execute(data),
        }

    # Busca uma pessoa específica pelo ID
    def show(self, data: TPessoaIdSchema):

        # Busca e retorna a pessoa desejada
        return {
            "message": "Pessoa localizado com sucesso",
            "data": TPessoaShowService().execute(data),
        }

    # Busca uma pessoa pelo nome
    def get_by_nome(self, data: TPessoaNameSchema):

        # Busca e retorna a pessoa desejada
        return {
            "message": "Pessoa localizado com sucesso",
            "data": TPessoaShowService().execute(data, True),
        }

    # Busca uma pessoa pelo e-mail
    def get_by_email(self, data: TPessoaEmailSchema):
        return {
            "message": "E-mail localizado com sucesso",
            "data": TPessoaGetEmailService().execute(data),
        }

    # Busca uma pessoa pelo CPF
    def get_by_cpf(self, data: TPessoaCpfSchema):
        return {
            "message": "CPF localizado com sucesso",
            "data": TPessoaGetCpfService().execute(data),
        }

    # Cadastra uma nova pessoa
    def save(self, data: TPessoaSaveSchema):

        # Salva os dados da pessoa e retorna o registro persistido
        return {
            "message": "Pessoa salvo com sucesso",
            "data": TPessoaSaveService().execute(data),
        }

    # Cadastra ou atualiza a foto de uma pessoa
    def save_foto(self, data: TPessoaSaveFotoSchema):

        # Salva a foto da pessoa e retorna o registro atualizado
        return {
            "message": "Pessoa salvo com sucesso",
            "data": TPessoaSaveFotoService().execute(data),
        }

    # Atualiza os dados de uma pessoa
    def update(self, data: TPessoaUpdateSchema):

        # Atualiza os dados da pessoa e retorna o registro persistido
        return {
            "message": "Pessoa atualizado com sucesso",
            "data": TPessoaUpdateService().execute(data),
        }

    # Exclui uma pessoa
    def delete(self, data: TPessoaIdSchema):

        # Remove a pessoa informada e retorna o resultado da operação
        return {
            "message": "Pessoa removido com sucesso",
            "data": TPessoaDeleteService().execute(data),
        }
