from packages.v1.sequencia.repositories.g_sequencia.checkout import Checkout
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from abstracts.action import BaseAction


class CheckoutAction(BaseAction):

    def execute(self, sequencia_schema: GSequenciaSchema):

        # Instânciamento de repositório
        checkout = Checkout()

        # Execução do repositório
        return checkout.execute(sequencia_schema)
