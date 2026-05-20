from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService
from packages.v1.administrativo.schemas.g_usuario_schema import GUsuarioSaveSchema, GUsuarioEmailSchema, GUsuarioCpfSchema
from packages.v1.administrativo.actions.g_usuario.g_usuario_save_action import SaveAction
from fastapi import status, HTTPException


class GUsuarioSaveService:

    def __init__(self):
        # Action responsável por carregar as services de acodo com o estado
        self.dynamic_import = DynamicImport()

        # Define o pacote que deve ser carregado
        self.dynamic_import.set_package("administrativo")

        # Define a tabela que o pacote pertence
        self.dynamic_import.set_table("g_usuario")
        pass    

    def execute(self, usuario_schema: GUsuarioSaveSchema):

        # Armazena possíveis erros
        errors = []

        # Verifica se o e-mail já esta sendo utilizado
        # Importação de service de email
        email_service = self.dynamic_import.service("g_usuario_get_email_service", "GetEmailService")

        # Instânciamento da service
        self.email_service = email_service()     

        # Verifica se o email já esta sendo utilizado
        self.response = self.email_service.execute(GUsuarioEmailSchema(email=usuario_schema.email), False)

        # Se houver retorno significa que o e-mail já esta sendo utiizado
        if self.response:
            errors.append({'input': 'email', 'message': 'O e-mail informado já está sendo utilizado.'})  

        # Verifica se o CPF já esta sendo utilizado
        # Importação de service de cpf
        cpf_service = self.dynamic_import.service("g_usuario_get_cpf_service", "GetCpfService")

        # Instânciamento da service
        self.cpf_service = cpf_service()     

        # Verifica se o cpf já esta sendo utilizado
        self.response = self.cpf_service.execute(GUsuarioCpfSchema(cpf=usuario_schema.cpf), False)

        # Se houver retorno significa que o cpf já esta sendo utiizado
        if self.response:
            errors.append({'input': 'cpf', 'message': 'O CPF informado já esta sendo utilizado.'})  

        # Verifica se o Login já esta sendo utilizado
        # Importação de service de login
        login_service = self.dynamic_import.service("g_usuario_get_login_service", "GetLoginService")

        # Instânciamento da service
        self.login_service = login_service()     

        # # Verifica se o login já esta sendo utilizado
        # self.response = self.login_service.execute(GUsuarioLoginSchema(login=usuario_schema.login), False)

        # # Se houver retorno significa que o login já esta sendo utilizado
        # if self.response:
        #     errors.append({'input': 'login', 'message': 'O login informado já está sendo utilizado.'})                    

        # Se houver erros, informo
        if errors:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=errors
            )        

        # Verifica se precisa gerar o id de sequencia
        if not usuario_schema.usuario_id:

            # Crio um objeto de sequencia
            sequencia_schema = GSequenciaSchema()

            # Define os dados para atualizar a sequencia
            sequencia_schema.tabela = 'G_USUARIO'

            # Busco a sequência atualizada
            generate = GenerateService()

            # Busco a sequência atualizada
            sequencia = generate.execute(sequencia_schema)

            # Atualiza os dados da chave primária
            usuario_schema.usuario_id = sequencia.sequencia

        # Instânciamento de ações
        saveAction = SaveAction()

        # Retorna todos produtos desejados
        return saveAction.execute(usuario_schema)