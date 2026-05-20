from packages.v1.administrativo.actions.c_caixa_item.c_caixa_item_update_action import UpdateAction
from packages.v1.administrativo.schemas.c_caixa_item_schema import CaixaItemSchema


class UpdateService:

    def execute(self, caixa_item_id : int, caixa_item_schema: CaixaItemSchema):

        # Instânciamento de ações
        updateAction = UpdateAction()

        # Retorna todos produtos desejados
        return updateAction.execute(caixa_item_id, caixa_item_schema)