from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.g_natureza_schema import (
    GNaturezaSaveSchema,
    GNaturezaSistemaIdSchema,
    GNaturezaUpdateSchema,
    GNaturezaIdSchema,
    GNaturezaDescricaoSchema
)

class GNaturezaController:

    def __init__(self):
        # Action responsável por carregar as services de acordo com o estado
        self.dynamic_import = DynamicImport()

        # Define o pacote que deve ser carregado
        self.dynamic_import.set_package("administrativo")

        # Define a tabela que o pacote pertence
        self.dynamic_import.set_table("g_natureza")
        pass

    # Lista todos os registros de natureza
    def index(self):
        
        # Importação da classe desejada
        indexService = self.dynamic_import.service("g_natureza_index_service", "IndexService")

        # Instância da classe service
        self.indexService = indexService()

        # Lista todos os registros de natureza
        return {
            'message': 'Registros de natureza localizados com sucesso',
            'data': self.indexService.execute()
        }

    # Lista todos os registros de natureza
    def indexBySistemaId(self, g_natureza_sistema_id_schema: GNaturezaSistemaIdSchema):
        
        # Importação da classe desejada
        indexService = self.dynamic_import.service("g_natureza_index_by_sistema_id_service", "IndexBySistemaIdService")

        # Instância da classe service
        self.indexService = indexService()

        # Lista todos os registros de natureza
        return {
            'message': 'Registros de natureza localizados com sucesso',
            'data': self.indexService.execute(g_natureza_sistema_id_schema)
        }
    
    
    # Busca um registro de natureza específico pelo ID
    def show(self, natureza_schema: GNaturezaIdSchema):

        #Importação da classe desejada
        show_service = self.dynamic_import.service('g_natureza_show_service', 'ShowService')

        # Instância da classe desejada
        self.show_service = show_service()

        # Busca e retorna o registro de natureza desejado
        return {
            'message': 'Registro de natureza localizado com sucesso',
            'data': self.show_service.execute(natureza_schema)
        }
    

    # Busca um registro de natureza pela descrição
    def get_by_descricao(self, natureza_schema: GNaturezaDescricaoSchema):

        #Importação da classe desejada
        show_service = self.dynamic_import.service('g_natureza_get_descricao_service', 'GetByDescricaoService')

        # Instância da classe desejada
        self.show_service = show_service()

        # Busca e retorna o registro de natureza desejado
        return {
            'message': 'Registro de natureza localizado com sucesso',
            'data': self.show_service.execute(natureza_schema, True)
        }  
              
    
    # Cadastra um novo registro de natureza
    def save(self, natureza_schema: GNaturezaSaveSchema):

        #Importação da classe desejada
        save_service = self.dynamic_import.service('g_natureza_save_service', 'SaveService')

        # Instância da classe desejada
        self.save_service = save_service()
        # Busca e retorna o registro de natureza desejado
        return {
            'message': 'Registro de natureza salvo com sucesso',
            'data': self.save_service.execute(natureza_schema)
        }
    
    # Atualiza os dados de um registro de natureza
    def update(self, natureza_id: int, natureza_schema: GNaturezaUpdateSchema):

        #Importação da classe desejada
        update_service = self.dynamic_import.service('g_natureza_update_service', 'UpdateService')

        # Instância da classe desejada
        self.update_service = update_service()

        # Busca e retorna o registro de natureza desejado
        return {
            'message': 'Registro de natureza atualizado com sucesso',
            'data': self.update_service.execute(natureza_id, natureza_schema)
        }
    
    # Exclui um registro de natureza
    def delete(self, natureza_schema: GNaturezaIdSchema):

        #Importação da classe desejada
        delete_service = self.dynamic_import.service('g_natureza_delete_service', 'DeleteService')

        # Instância da classe desejada
        self.delete_service = delete_service()

        # Busca e retorna o registro de natureza desejado
        return {
            'message': 'Registro de natureza removido com sucesso',
            'data': self.delete_service.execute(natureza_schema)
        }