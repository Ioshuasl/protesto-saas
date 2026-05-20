from packages.v1.administrativo.actions.c_caixa_item.c_caixa_item_index_action import IndexAction


class IndexService:

    def execute(self):

        # Instânciamento de ações
        indexAction = IndexAction()

        # Retorna todos produtos desejados
        return indexAction.execute()