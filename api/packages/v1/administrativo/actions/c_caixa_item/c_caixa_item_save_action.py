from packages.v1.administrativo.repositories.c_caixa_item.c_caixa_item_save import Save
from packages.v1.administrativo.schemas.c_caixa_item_schema import \
    CaixaItemSchema
from abstracts.action import BaseAction


class SaveAction(BaseAction):

    def execute(self, caixa_item_schema : CaixaItemSchema):

        # Instância o repositório desejado
        save = Save()

        # Executa o respositório desejado
        return save.execute(caixa_item_schema)