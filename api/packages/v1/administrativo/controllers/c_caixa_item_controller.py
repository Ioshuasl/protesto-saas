# Importação de bibliotecas
from packages.v1.administrativo.schemas.c_caixa_item_schema import CaixaItemSchema
from actions.dynamic_import.dynamic_import import DynamicImport


class CCaixaItemController:

    def __init__(self):
        # Classe responsável por carregar as services de acordo com o estado
        self.dynamic_import = DynamicImport()
        # Define o pacote que deve ser carregado
        self.dynamic_import.set_package("administrativo")
        # Define a tabela que o pacote pertence
        self.dynamic_import.set_table("c_caixa_item")

    def index(self):

        # Importação da classe desejad
        indexService = self.dynamic_import.service("c_caixa_item_index_service", "IndexService")

        # Intânciamento da classe service
        self.indexService = indexService()

        # Lista todos os produtos
        return {
            'message' : 'Registros localizados com sucesso',
            'data': self.indexService.execute()
        }

    def create(self, caixa_item_schema: CaixaItemSchema):

        # Importação da classe desejada
        createService = self.dynamic_import.service("c_caixa_item_save_service", "SaveService")

        # Intânciamento da classe service
        self.createService = createService()

        # Lista todos os produtos
        return {
            'message' : 'Registros cadastrado com sucesso',
            'data': self.createService.execute(caixa_item_schema)
        }
    

    def update(self, caixa_item_id : int, caixa_item_schema: CaixaItemSchema):

        # Importação da classe desejada
        updateService = self.dynamic_import.service("c_caixa_item_update_service", "UpdateService")

        # Intânciamento da classe service
        self.updateService = updateService()

        # Lista todos os produtos
        return {
            'message' : 'Registros cadastrado com sucesso',
            'data': self.updateService.execute(caixa_item_id, caixa_item_schema)
        }    
    

    def show(self, caixa_item_schema: CaixaItemSchema):
        # Importação da classe desejad
        showService = self.dynamic_import.service("c_caixa_item_show_service", "ShowService")

        # Intânciamento da classe service
        self.showService = showService()

        # Lista todos os produtos
        return {
            'message' : 'Registro localizado com sucesso',
            'data': self.showService.execute(caixa_item_schema)
        }

    def delete(self, caixa_item_schema: CaixaItemSchema):
        # Importação da classe desejad
        deleteService = self.dynamic_import.service("c_caixa_item_delete_service", "DeleteService")

        # Intânciamento da classe service
        self.deleteService = deleteService()

        # Lista todos os produtos
        return {
            'message' : 'Registros removido com sucesso',
            'data': self.deleteService.execute(caixa_item_schema)
        }