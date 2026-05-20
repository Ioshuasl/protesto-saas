from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService
from packages.v1.administrativo.schemas.g_tb_txmodelogrupo_schema import GTbTxmodelogrupoSaveSchema, GTbTxmodelogrupoDescricaoSchema
from packages.v1.administrativo.actions.g_tb_txmodelogrupo.g_tb_txmodelogrupo_save_action import SaveAction
from fastapi import HTTPException, status

class GTbTxmodelogrupoSaveService:

    def __init__(self):
        # Action responsável por carregar as services de acordo com o estado
        self.dynamic_import = DynamicImport()

        # Define o pacote que deve ser carregado
        self.dynamic_import.set_package("administrativo")

        # Define a tabela que o pacote pertence
        self.dynamic_import.set_table("g_tb_txmodelogrupo")
        pass

    # Cadastra o novo modelo de grupo serviço
    def execute(self, txmodelogrupo_schema: GTbTxmodelogrupoSaveSchema):

        # Armazena possíveis erros
        errors = []

        # Verifica se a descrição já está sendo utilizada
        # Importação de service de get_by_descricao
        get_by_descricao_service = self.dynamic_import.service("g_tb_txmodelogrupo_get_by_descricao_service", "GetByDescricaoService")

        # Instanciamento da service
        self.get_by_descricao_service = get_by_descricao_service()

        # Verifica se a descrição já está sendo utilizada
        self.response = self.get_by_descricao_service.execute(GTbTxmodelogrupoDescricaoSchema(descricao=txmodelogrupo_schema.descricao), False)

        # Se houver retorno significa que a descrição já está sendo utilizada
        if self.response:
            errors.append({'input': 'descricao', 'message': 'A descrição informada já está sendo utilizada.'})

        # Se houver erros, informo
        if errors:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=errors
            )

        # Verifica se precisa gerar o id de sequência
        if not txmodelogrupo_schema.tb_txmodelogrupo_id:

            # Crio um objeto de sequencia
            sequencia_schema = GSequenciaSchema()

            # Define os dados para atualizar a sequência
            sequencia_schema.tabela = 'G_TB_TXMODELOGRUPO'

            # Busco a sequência atualizada
            generate_service = GenerateService()

            # Busco a sequência atualizada
            sequencia = generate_service.execute(sequencia_schema)

            # Atualiza os dados da chave primária
            txmodelogrupo_schema.tb_txmodelogrupo_id = sequencia.sequencia

        # Instânciamento de ações
        saveAction = SaveAction()

        # Retorna todos os produtos desejados
        return saveAction.execute(txmodelogrupo_schema)