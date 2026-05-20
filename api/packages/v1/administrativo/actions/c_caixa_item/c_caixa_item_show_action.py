from packages.v1.administrativo.repositories.c_caixa_item.c_caixa_item_show import Show
from packages.v1.administrativo.schemas.c_caixa_item_schema import CaixaItemSchema
from abstracts.action import BaseAction


class ShowAction(BaseAction):

    def execute(self, caixa_item_schema : CaixaItemSchema):

        # Instânciamento do repositório
        show = Show()

        # Retorna os dados localizados
        return show.execute(caixa_item_schema)