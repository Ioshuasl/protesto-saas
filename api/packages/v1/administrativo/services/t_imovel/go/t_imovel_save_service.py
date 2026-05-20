from datetime import datetime
from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.actions.t_imovel.t_imovel_save_action import (
    TImovelSaveAction,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.administrativo.schemas.t_imovel_schema import TImovelSaveSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService


class TImovelSaveService:

    def __init__(self):
        # Ação responsável por carregar as services de acordo com o estado
        self.dynamic_import = DynamicImport()

        # Define o pacote que deve ser carregado
        self.dynamic_import.set_package("administrativo")

        # Define a tabela que o pacote pertence
        self.dynamic_import.set_table("t_imovel")
        pass

    # Cadastra o novo CENSEC_QUALIDADE
    def execute(self, t_imovel_save_schema: TImovelSaveSchema):

        t_imovel_save_schema.data_registro = datetime.now()

        # Verifica se precisa gerar o ID de sequência
        # Coluna primária ajustadaA
        if not t_imovel_save_schema.imovel_id:

            # Crio um objeto de sequencia
            sequencia_schema = GSequenciaSchema()

            # Define os dados para atualizar a sequencia
            sequencia_schema.tabela = "T_IMOVEL"

            # Busco a sequência atualizada
            generate = GenerateService()

            # Busco a sequência atualizada
            sequencia = generate.execute(sequencia_schema)

            # Atualiza os dados da chave primária
            t_imovel_save_schema.imovel_id = sequencia.sequencia

        # Instanciamento de ações
        # Ação já é importada como SaveAction
        t_imovel_save_action = TImovelSaveAction()

        # Retorna o resultado da operação
        return t_imovel_save_action.execute(
            t_imovel_save_schema
        )  # Nome do parâmetro ajustado
