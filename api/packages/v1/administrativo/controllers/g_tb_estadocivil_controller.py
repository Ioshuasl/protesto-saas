from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.g_tb_estadocivil_schema import (
    GTbEstadoCivilSaveSchema,
    GTbEstadoCivilUpdateSchema,
    GTbEstadoCivilIdSchema,
    GTbEstadoCivilDescricaoSchema
)

class GTbEstadoCivilController:

    def __init__(self):
        # Action responsável por carregar as services de acordo com o estado
        self.dynamic_import = DynamicImport()

        # Define o pacote que deve ser carregado
        self.dynamic_import.set_package("administrativo")

        # Define a tabela que o pacote pertence
        self.dynamic_import.set_table("g_tb_estadocivil")
        pass

    # Lista todos os registros de estadocivil
    def index(self):
        
        # Importação da classe desejada
        indexService = self.dynamic_import.service("g_tb_estadocivil_index_service", "IndexService")

        # Instância da classe service
        self.indexService = indexService()

        # Lista todos os registros de estadocivil
        return {
            'message': 'Registros de estadocivil localizados com sucesso',
            'data': self.indexService.execute()
        }
    
    
    # Busca um registro de estadocivil específico pelo ID
    def show(self, estadocivil_schema: GTbEstadoCivilIdSchema):

        #Importação da classe desejada
        show_service = self.dynamic_import.service('g_tb_estadocivil_show_service', 'ShowService')

        # Instância da classe desejada
        self.show_service = show_service()

        # Busca e retorna o registro de estadocivil desejado
        return {
            'message': 'Registro de estadocivil localizado com sucesso',
            'data': self.show_service.execute(estadocivil_schema)
        }
    

    # Busca um registro de estadocivil pela descrição
    def get_by_descricao(self, estadocivil_schema: GTbEstadoCivilDescricaoSchema):

        #Importação da classe desejada
        show_service = self.dynamic_import.service('g_tb_estadocivil_get_descricao_service', 'GetByDescricaoService')

        # Instância da classe desejada
        self.show_service = show_service()

        # Busca e retorna o registro de estadocivil desejado
        return {
            'message': 'Registro de estadocivil localizado com sucesso',
            'data': self.show_service.execute(estadocivil_schema, True)
        }  
              
    
    # Cadastra um novo registro de estadocivil
    def save(self, estadocivil_schema: GTbEstadoCivilSaveSchema):

        #Importação da classe desejada
        save_service = self.dynamic_import.service('g_tb_estadocivil_save_service', 'SaveService')

        # Instância da classe desejada
        self.save_service = save_service()
        # Busca e retorna o registro de estadocivil desejado
        return {
            'message': 'Registro de estadocivil salvo com sucesso',
            'data': self.save_service.execute(estadocivil_schema)
        }
    
    # Atualiza os dados de um registro de estadocivil
    def update(self, tb_estadocivil_id: int, estadocivil_schema: GTbEstadoCivilUpdateSchema):

        #Importação da classe desejada
        update_service = self.dynamic_import.service('g_tb_estadocivil_update_service', 'UpdateService')

        # Instância da classe desejada
        self.update_service = update_service()

        # Busca e retorna o registro de estadocivil desejado
        return {
            'message': 'Registro de estadocivil atualizado com sucesso',
            'data': self.update_service.execute(tb_estadocivil_id, estadocivil_schema)
        }
    
    # Exclui um registro de estadocivil
    def delete(self, estadocivil_schema: GTbEstadoCivilIdSchema):

        #Importação da classe desejada
        delete_service = self.dynamic_import.service('g_tb_estadocivil_delete_service', 'DeleteService')

        # Instância da classe desejada
        self.delete_service = delete_service()

        # Busca e retorna o registro de estadocivil desejado
        return {
            'message': 'Registro de estadocivil removido com sucesso',
            'data': self.delete_service.execute(estadocivil_schema)
        }