from packages.v1.sequencia.actions.g_sequencia.checkout_action import CheckoutAction
from packages.v1.sequencia.actions.g_sequencia.get_action import GetAction
from packages.v1.sequencia.actions.g_sequencia.save_action import SaveAction
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema


class GenerateService:

    def execute(self, sequencia_schema: GSequenciaSchema):

        # Instânciamento de Action
        getAction = GetAction()
        saveAction = SaveAction()
        checkoutAction = CheckoutAction()

        # Verifico se a tabela existe no G_SEQUENCIA e se a sequência está correta
        checkoutAction.execute(sequencia_schema)

        # Busco a sequência atual
        sequencia_result = getAction.execute(sequencia_schema)

        # Incrementa a sequência atual
        sequencia_schema.sequencia = sequencia_result.sequencia + 1

        # Atualiza a sequência atual
        return saveAction.execute(sequencia_schema)
