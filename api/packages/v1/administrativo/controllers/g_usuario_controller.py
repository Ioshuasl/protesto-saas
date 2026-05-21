from fastapi import Request
from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.g_usuario_schema import (
    GUsuarioIndexSchema,
    GUsuarioSchema,
    GUsuarioAuthenticateSchema,
    GUsuarioSaveSchema,
    GUsuarioUpdateSchema,
    GUsuarioEmailSchema,
    GUsuarioCpfSchema,
    GUsuarioLoginSchema,
    GUsuarioIdSchema,
)


class GUsuarioController:

    def __init__(self):
        # Action responsável por carregar as services de acodo com o estado
        self.dynamic_import = DynamicImport()

        # Define o pacote que deve ser carregado
        self.dynamic_import.set_package("administrativo")

        # Define a tabela que o pacote pertence
        self.dynamic_import.set_table("g_usuario")
        pass

    # Efetua o acesso junto ao sistema por um determinado usuário
    def authenticate(
        self,
        g_usuario_authenticate_schema: GUsuarioAuthenticateSchema,
        request: Request,
    ):

        # Importação de service de Authenticate
        authenticate_service = self.dynamic_import.service(
            "g_usuario_authenticate_service", "AuthenticateService"
        )

        # Instânciamento da service
        self.authenticate_service = authenticate_service()

        result = self.authenticate_service.execute(
            g_usuario_authenticate_schema=g_usuario_authenticate_schema,
            request=request,
        )

        # Token (str) após login completo; dict na etapa de desafio 2FA
        data = {"token": result} if isinstance(result, str) else result

        return {
            "message": "Usuário localizado com sucesso",
            "data": data,
        }

    # Carrega os dados do usuário logado
    def me(self, current_user):

        # Importação de service de authenticate
        me_service = self.dynamic_import.service("g_usuario_me_service", "MeService")

        # Instânciamento da service
        self.me_service = me_service()

        # Retorna o usuário logado
        return {
            "message": "Usuário localizado com sucesso",
            "data": self.me_service.execute(current_user),
        }

    # Lista todos os usuários
    def index(self, g_usuario_index_schema: GUsuarioIndexSchema):

        # Importação da classe desejada
        indexService = self.dynamic_import.service(
            "g_usuario_index_service", "IndexService"
        )

        # Instânciamento da classe service
        self.indexService = indexService()

        # Lista todos os usuários
        return {
            "message": "Usuários localizados com sucesso",
            "data": self.indexService.execute(g_usuario_index_schema),
        }

    # Busca um usuário especifico pelo ID
    def show(self, usuario_schema: GUsuarioSchema):

        # Importação da classe desejada
        show_service = self.dynamic_import.service(
            "g_usuario_show_service", "ShowService"
        )

        # Instânciamento da classe desejada
        self.show_service = show_service()

        # Busca e retorna o usuário desejado
        return {
            "message": "Usuário localizado com sucesso",
            "data": self.show_service.execute(usuario_schema),
        }

    # Busca um usuário especifico pelo e-mail
    def getEmail(self, usuario_schema: GUsuarioEmailSchema):

        # Importação da classe desejada
        get_email_service = self.dynamic_import.service(
            "g_usuario_get_email_service", "GetEmailService"
        )

        # Instânciamento da classe desejada
        self.get_email_service = get_email_service()

        # Busca e retorna o usuário desejado
        return {
            "message": "E-mail localizado com sucesso",
            "data": self.get_email_service.execute(
                usuario_schema, True
            ),  # True para retornar a mensagem de erro caso não localize o usuario
        }

    # Busca um usuário especifico pelo e-mail
    def getLogin(self, usuario_schema: GUsuarioLoginSchema):

        # Importação da classe desejada
        get_login_service = self.dynamic_import.service(
            "g_usuario_get_login_service", "GetLoginService"
        )

        # Instânciamento da classe desejada
        self.get_login_service = get_login_service()

        # Busca e retorna o usuário desejado
        return {
            "message": "Login localizado com sucesso",
            "data": self.get_login_service.execute(
                usuario_schema, True
            ),  # True para retornar a mensagem de erro caso não localize o usuario
        }

    # Busca um usuário especifico pelo CPF
    def getCpf(self, usuario_schema: GUsuarioCpfSchema):

        # Importação da classe desejada
        get_cpf_service = self.dynamic_import.service(
            "g_usuario_get_cpf_service", "GetCpfService"
        )

        # Instânciamento da classe desejada
        self.get_cpf_service = get_cpf_service()

        # Busca e retorna o usuário desejado
        return {
            "message": "CPF localizado com sucesso",
            "data": self.get_cpf_service.execute(
                usuario_schema, True
            ),  # True para retornar a mensagem de erro caso não localize o usuario
        }

    # Cadastra um novo usuário
    def save(self, usuario_schema: GUsuarioSaveSchema):

        # Importação da classe desejada
        save_service = self.dynamic_import.service(
            "g_usuario_save_service", "GUsuarioSaveService"
        )

        # Instânciamento da classe desejada
        self.save_service = save_service()

        # Busca e retorna o usuário desejado
        return {
            "message": "Usuário salvo com sucesso.",
            "data": self.save_service.execute(usuario_schema),
        }

    # Atualiza os dados de um usuário
    def update(self, usuario_id: int, usuario_schema: GUsuarioUpdateSchema):

        # Importação da classe desejada
        save_service = self.dynamic_import.service(
            "g_usuario_update_service", "GUsuarioUpdateService"
        )

        # Instânciamento da classe desejada
        self.save_service = save_service()

        # Busca e retorna o usuário desejado
        return {

            "message": "Usuário atualizado com sucesso",
            "data": self.save_service.execute(usuario_id, usuario_schema),
        }

    # Exclui um usuário
    def delete(self, usuario_schema: GUsuarioIdSchema):

        # Importação da classe desejada
        delete_service = self.dynamic_import.service(
            "g_usuario_delete_service", "DeleteService"
        )

        # Instânciamento da classe desejada
        self.delete_service = delete_service()

        # Busca e retorna o usuário desejado
        return {
            "message": "Usuário removido com sucesso",
            "data": self.delete_service.execute(usuario_schema),
        }
