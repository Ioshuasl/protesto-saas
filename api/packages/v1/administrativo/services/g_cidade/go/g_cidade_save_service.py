from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService
from packages.v1.administrativo.schemas.g_cidade_schema import GCidadeSaveSchema, GCidadeNomeSchema
from packages.v1.administrativo.actions.g_cidade.g_cidade_save_action import SaveAction
from fastapi import HTTPException, status

class SaveService:

    def __init__(self):
        # Action responsável por carregar as services de acordo com o estado
        self.dynamic_import = DynamicImport()

        # Define o pacote que deve ser carregado
        self.dynamic_import.set_package("administrativo")

        # Define a tabela que o pacote pertence
        self.dynamic_import.set_table("g_cidade")
        pass

    # Cadastra o novo G_CIDADE
    def execute(self, g_cidade_schema: GCidadeSaveSchema):

        # Armazena possíveis erros
        errors = []

        # Verifica se o nome da cidade já está sendo utilizada
        # Importação de service
        nome_service = self.dynamic_import.service("g_cidade_get_nome_service", "GetByNomeService")

        # Instanciamento da service
        self.nome_service = nome_service()

        # Verifica se o nome da cidade já está sendo utilizada
        self.response = self.nome_service.execute(GCidadeNomeSchema(cidade_nome=g_cidade_schema.cidade_nome), False)

        # Se houver retorno significa que o nome da cidade já está sendo utilizado
        if self.response:
            errors.append({'input': 'cidade_nome', 'message': 'O nome da cidade informado já está sendo utilizado.'})

        # Se houver erros, lança a exceção
        if errors:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=errors
            )

        # Verifica se precisa gerar o ID de sequência
        if not g_cidade_schema.cidade_id:

            # Crio um objeto de sequencia
            sequencia_schema = GSequenciaSchema()

            # Define os dados para atualizar a sequencia
            sequencia_schema.tabela = 'G_CIDADE' # Nome da tabela para a sequência

            # Busco a sequência atualizada
            generate = GenerateService()

            # Busco a sequência atualizada
            sequencia = generate.execute(sequencia_schema)

            # Atualiza os dados da chave primária
            g_cidade_schema.cidade_id = sequencia.sequencia

        # Instanciamento de ações
        save_action = SaveAction()

        # Retorna o resultado da operação
        return save_action.execute(g_cidade_schema)