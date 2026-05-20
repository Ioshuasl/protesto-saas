from packages.v1.administrativo.repositories.c_caixa_item.c_caixa_item_delete import Delete
from packages.v1.administrativo.schemas.c_caixa_item_schema import CaixaItemSchema
from abstracts.action import BaseAction


class DeleteAction(BaseAction):

    def execute(self, caixa_item_schema: CaixaItemSchema):

        # Instânciamento de repoistório
        delete = Delete()

        # Retorna o resultado da operação
        return delete.execute(caixa_item_schema)