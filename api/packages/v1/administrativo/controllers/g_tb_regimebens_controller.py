from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.g_tb_regimebens_schema import (
    GTbRegimebensSaveSchema,
    GTbRegimebensUpdateSchema,
    GTbRegimebensIdSchema,
    GTbRegimebensDescricaoSchema
)

class GTbRegimebensController:

    def __init__(self):
        # Action responsável por carregar as services de acordo com o estado
        self.dynamic_import = DynamicImport()

        # Define o pacote que deve ser carregado
        self.dynamic_import.set_package("administrativo")

        # Define a tabela que o pacote pertence
        self.dynamic_import.set_table("g_tb_regimebens")
        pass

    # Lista todos os regimes de bens
    def index(self):
        
        # Importação da classe desejada
        indexService = self.dynamic_import.service("g_tb_regimebens_index_service", "IndexService")

        # Instância da classe service
        self.indexService = indexService()

        # Lista todos os regimes de bens
        return {
            'message': 'Regimes de bens localizados com sucesso',
            'data': self.indexService.execute()
        }
    
    
    # Busca um regime de bens específico pelo ID
    def show(self, regimebens_schema : GTbRegimebensIdSchema):

        #Importação da classe desejada
        show_service = self.dynamic_import.service('g_tb_regimebens_show_service', 'ShowService')

        # Instância da classe desejada
        self.show_service = show_service()

        # Busca e retorna o regime de bens desejado
        return {
            'message' : 'Regime de bens localizado com sucesso',
            'data': self.show_service.execute(regimebens_schema)
        }
    

    # Busca um regime de bens pela descrição
    def get_by_descricao(self, regimebens_schema : GTbRegimebensDescricaoSchema):

        #Importação da classe desejada
        show_service = self.dynamic_import.service('g_tb_regimebens_get_descricao_service', 'GetByDescricaoService')

        # Instância da classe desejada
        self.show_service = show_service()

        # Busca e retorna o regime de bens desejado
        return {
            'message' : 'Regime de bens localizado com sucesso',
            'data': self.show_service.execute(regimebens_schema, True)
        }  
              
    
    # Cadastra um novo regime de bens
    def save(self, regimebens_schema : GTbRegimebensSaveSchema):

        #Importação da classe desejada
        save_service = self.dynamic_import.service('g_tb_regimebens_save_service', 'GTbRegimebensSaveService')

        # Instância da classe desejada
        self.save_service = save_service()
        # Busca e retorna o regime de bens desejado
        return {
            'message' : 'Regime de bens salvo com sucesso',
            'data': self.save_service.execute(regimebens_schema)
        }
    
    # Atualiza os dados de um regime de bens
    def update(self, tb_regimebens_id : int, regimebens_schema : GTbRegimebensUpdateSchema):

        #Importação da classe desejada
        update_service = self.dynamic_import.service('g_tb_regimebens_update_service', 'GTbRegimebensUpdateService')

        # Instância da classe desejada
        self.update_service = update_service()

        # Busca e retorna o regime de bens desejado
        return {
            'message' : 'Regime de bens atualizado com sucesso',
            'data': self.update_service.execute(tb_regimebens_id, regimebens_schema)
        }
    
    # Exclui um regime de bens
    def delete(self, regimebens_schema : GTbRegimebensIdSchema):

        #Importação da classe desejada
        delete_service = self.dynamic_import.service('g_tb_regimebens_delete_service', 'DeleteService')

        # Instância da classe desejada
        self.delete_service = delete_service()

        # Busca e retorna o regime de bens desejado
        return {
            'message' : 'Regime de bens removido com sucesso',
            'data': self.delete_service.execute(regimebens_schema)
        }