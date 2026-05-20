from packages.v1.sequencia.actions.g_sequencia.checkout_action import CheckoutAction
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from fastapi import HTTPException, status


class GenerateService:

    def execute(self, sequencia_schema : GSequenciaSchema):

        # Instânciamento de Action
        checkoutAction = CheckoutAction()
        
        # Atualiza a sequência atual
        data = checkoutAction.execute(sequencia_schema)
    
        # Verifica se foi localizado o registro
        if not data:
            # Retorna uma exceção
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Não foi possível localizar a tabela para verificação de sequência'
            )

        # Retorna a informação localizada
        return data
