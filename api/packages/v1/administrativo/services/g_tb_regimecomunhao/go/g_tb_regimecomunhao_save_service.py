from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService
from packages.v1.administrativo.schemas.g_tb_regimecomunhao_schema import GTbRegimecomunhaoSaveSchema, GTbRegimecomunhaoDescricaoSchema
from packages.v1.administrativo.actions.g_tb_regimecomunhao.g_tb_regimecomunhao_save_action import SaveAction
from fastapi import HTTPException, status

class GTbRegimecomunhaoSaveService:

    def __init__(self):
        # Action responsável por carregar as services de acodo com o estado
        self.dynamic_import = DynamicImport()

        # Define o pacote que deve ser carregado
        self.dynamic_import.set_package("administrativo")

        # Define a tabela que o pacote pertence
        self.dynamic_import.set_table("g_tb_regimecomunhao")
        pass    

    # Cadastra o novo caixa serviço
    def execute(self, regimecomunhao_schema: GTbRegimecomunhaoSaveSchema):  

        # Armazena possíveis erros
        errors = []

        # Verifica se o e-mail já esta sendo utilizado
        # Importação de service de email
        descricao_service = self.dynamic_import.service("g_tb_regimecomunhao_get_by_descricao_service", "GetByDescricaoService")

        # Instânciamento da service
        self.descricao_service = descricao_service()     

        # Verifica se a descrição já está sendo utilizada
        self.response = self.descricao_service.execute(GTbRegimecomunhaoDescricaoSchema(descricao=regimecomunhao_schema.descricao), False)

        # Se houver retorno significa que a descrição já esta sendo utiizada
        if self.response:
            errors.append({'input': 'descricao', 'message': 'a descrição informada já está sendo utilizada.'})  

        # Se houver erros, informo
        if errors:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=errors
            ) 
        

        # Verifica se precisa gerar o id de sequencia
        if not regimecomunhao_schema.tb_regimecomunhao_id:

            # Crio um objeto de sequencia
            sequencia_schema = GSequenciaSchema()

            # Define os dados para atualizar a sequencia
            sequencia_schema.tabela = 'G_TB_REGIMECOMUNHAO'

            # Busco a sequência atualizada
            generate = GenerateService()

            # Busco a sequência atualizada
            sequencia = generate.execute(sequencia_schema)

            # Atualiza os dados da chave primária
            regimecomunhao_schema.tb_regimecomunhao_id = sequencia.sequencia

        # Instânciamento de ações
        saveAction = SaveAction()

        # Retorna todos produtos desejados
        return saveAction.execute(regimecomunhao_schema)