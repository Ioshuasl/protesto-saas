from packages.v1.administrativo.repositories.c_caixa_item.c_caixa_item_index import \
    Index
from abstracts.action import BaseAction


class IndexAction(BaseAction):

    def execute(self):

        # Instânciamento de repositório
        index = Index()

        # Retorna todos produtos
        return index.execute()