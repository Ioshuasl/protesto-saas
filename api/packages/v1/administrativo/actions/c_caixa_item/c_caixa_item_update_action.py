from packages.v1.administrativo.repositories.c_caixa_item.c_caixa_item_update_repository import UpdateRepository
from packages.v1.administrativo.schemas.c_caixa_item_schema import CaixaItemSchema
from abstracts.action import BaseAction


class UpdateAction(BaseAction):

    def execute(self, caixa_item_id : int, caixa_item_schema : CaixaItemSchema):

        # Instância o repositório desejado
        update = UpdateRepository()

        # Executa o respositório desejado
        return update.execute(caixa_item_id, caixa_item_schema)