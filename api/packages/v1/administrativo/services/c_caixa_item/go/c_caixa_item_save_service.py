from packages.v1.administrativo.actions.c_caixa_item.c_caixa_item_save_action import (
    SaveAction,
)
from packages.v1.administrativo.schemas.c_caixa_item_schema import CaixaItemSchema
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService


class SaveService:

    def execute(self, caixa_item_schema: CaixaItemSchema):

        # Crio um objeto de sequencia
        sequencia_schema = GSequenciaSchema()

        # Define os dados para atualizar a sequencia
        sequencia_schema.tabela = "C_CAIXA_ITEM"

        # Busco a sequência atualizada
        generate = GenerateService()

        # Busco a sequência atualizada
        sequencia = generate.execute(sequencia_schema)

        # Atualiza os dados da chave primária
        caixa_item_schema.caixa_item_id = sequencia.sequencia

        # Instânciamento de ações
        saveAction = SaveAction()

        # Retorna todos produtos desejados
        return saveAction.execute(caixa_item_schema)
