from fastapi import HTTPException, status
from packages.v1.administrativo.actions.c_caixa_item.c_caixa_item_show_action import ShowAction
from packages.v1.administrativo.schemas.c_caixa_item_schema import CaixaItemSchema

class ShowService:

    def execute(self, caixa_item_schema: CaixaItemSchema):

        # Instânciamento de ações
        showAction = ShowAction()

        # Retorna todos produtos desejados
        data = showAction.execute(caixa_item_schema)

        # Verifica se foi localizado o registro
        if not data:
            # Retorna uma exceção
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Não foi possível localizar o registro'
            )

        # Retorna a informação localizada
        return data
