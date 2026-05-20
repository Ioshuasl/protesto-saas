from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.g_medida_tipo_schema import (
    GMedidaTipoSaveSchema,
    GMedidaTipoUpdateSchema,
    GMedidaTipoIdSchema,
    GMedidaTipoDescricaoSchema
)

class GMedidaTipoController:

    def __init__(self):
        # Action responsável por carregar as services de acordo com o estado
        self.dynamic_import = DynamicImport()

        # Define o pacote que deve ser carregado
        self.dynamic_import.set_package("administrativo")

        # Define a tabela que o pacote pertence
        self.dynamic_import.set_table("g_medida_tipo")
        pass

    # Lista todos os registros de g_medida_tipo
    def index(self):
        
        # Importação da classe desejada
        indexService = self.dynamic_import.service("g_medida_tipo_index_service", "IndexService")

        # Instância da classe service
        self.indexService = indexService()

        # Lista todos os registros de g_medida_tipo
        return {
            'message': 'Registros de g_medida_tipo localizados com sucesso',
            'data': self.indexService.execute()
        }
    
    
    # Busca um registro de g_medida_tipo específico pelo ID
    def show(self, medida_tipo_schema: GMedidaTipoIdSchema):

        #Importação da classe desejada
        show_service = self.dynamic_import.service('g_medida_tipo_show_service', 'ShowService')

        # Instância da classe desejada
        self.show_service = show_service()

        # Busca e retorna o registro de g_medida_tipo desejado
        return {
            'message': 'Registro de g_medida_tipo localizado com sucesso',
            'data': self.show_service.execute(medida_tipo_schema)
        }
    

    # Busca um registro de g_medida_tipo pela descrição
    def get_by_descricao(self, medida_tipo_schema: GMedidaTipoDescricaoSchema):

        #Importação da classe desejada
        show_service = self.dynamic_import.service('g_medida_tipo_get_descricao_service', 'GetByDescricaoService')

        # Instância da classe desejada
        self.show_service = show_service()

        # Busca e retorna o registro de g_medida_tipo desejado
        return {
            'message': 'Registro de g_medida_tipo localizado com sucesso',
            'data': self.show_service.execute(medida_tipo_schema, True)
        }  
              
    
    # Cadastra um novo registro de g_medida_tipo
    def save(self, medida_tipo_schema: GMedidaTipoSaveSchema):

        #Importação da classe desejada
        save_service = self.dynamic_import.service('g_medida_tipo_save_service', 'SaveService')

        # Instância da classe desejada
        self.save_service = save_service()
        # Busca e retorna o registro de g_medida_tipo desejado
        return {
            'message': 'Registro de g_medida_tipo salvo com sucesso',
            'data': self.save_service.execute(medida_tipo_schema)
        }
    
    # Atualiza os dados de um registro de g_medida_tipo
    def update(self, medida_tipo_id: int, medida_tipo_schema: GMedidaTipoUpdateSchema):

        #Importação da classe desejada
        update_service = self.dynamic_import.service('g_medida_tipo_update_service', 'UpdateService')

        # Instância da classe desejada
        self.update_service = update_service()

        # Busca e retorna o registro de g_medida_tipo desejado
        return {
            'message': 'Registro de g_medida_tipo atualizado com sucesso',
            'data': self.update_service.execute(medida_tipo_id, medida_tipo_schema)
        }
    
    # Exclui um registro de g_medida_tipo
    def delete(self, medida_tipo_schema: GMedidaTipoIdSchema):

        #Importação da classe desejada
        delete_service = self.dynamic_import.service('g_medida_tipo_delete_service', 'DeleteService')

        # Instância da classe desejada
        self.delete_service = delete_service()

        # Busca e retorna o registro de g_medida_tipo desejado
        return {
            'message': 'Registro de g_medida_tipo removido com sucesso',
            'data': self.delete_service.execute(medida_tipo_schema)
        }