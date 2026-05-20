from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.t_censec_schema import (
    TCensecSaveSchema,
    TCensecUpdateSchema,
    TCensecIdSchema,
    TCensecDescricaoSchema
)

class TCensecController:

    def __init__(self):
        # Action responsável por carregar as services de acordo com o estado
        self.dynamic_import = DynamicImport()

        # Define o pacote que deve ser carregado
        self.dynamic_import.set_package("administrativo")

        # Define a tabela que o pacote pertence
        self.dynamic_import.set_table("t_censec")
        pass

    # Lista todos os registros de censec
    def index(self):
        
        # Importação da classe desejada
        indexService = self.dynamic_import.service("t_censec_index_service", "IndexService")

        # Instância da classe service
        self.indexService = indexService()

        # Lista todos os registros de censec
        return {
            'message': 'Registros de censec localizados com sucesso',
            'data': self.indexService.execute()
        }
    
    
    # Busca um registro de censec específico pelo ID
    def show(self, censec_schema: TCensecIdSchema):

        #Importação da classe desejada
        show_service = self.dynamic_import.service('t_censec_show_service', 'ShowService')

        # Instância da classe desejada
        self.show_service = show_service()

        # Busca e retorna o registro de censec desejado
        return {
            'message': 'Registro de censec localizado com sucesso',
            'data': self.show_service.execute(censec_schema)
        }
    

    # Busca um registro de censec pela descrição
    def get_by_descricao(self, censec_schema: TCensecDescricaoSchema):

        #Importação da classe desejada
        show_service = self.dynamic_import.service('t_censec_get_descricao_service', 'GetByDescricaoService')

        # Instância da classe desejada
        self.show_service = show_service()

        # Busca e retorna o registro de censec desejado
        return {
            'message': 'Registro de censec localizado com sucesso',
            'data': self.show_service.execute(censec_schema, True)
        }  
              
    
    # Cadastra um novo registro de censec
    def save(self, censec_schema: TCensecSaveSchema):

        #Importação da classe desejada
        save_service = self.dynamic_import.service('t_censec_save_service', 'SaveService')

        # Instância da classe desejada
        self.save_service = save_service()
        # Busca e retorna o registro de censec desejado
        return {
            'message': 'Registro de censec salvo com sucesso',
            'data': self.save_service.execute(censec_schema)
        }
    
    # Atualiza os dados de um registro de censec
    def update(self, censec_id: int, censec_schema: TCensecUpdateSchema):

        #Importação da classe desejada
        update_service = self.dynamic_import.service('t_censec_update_service', 'UpdateService')

        # Instância da classe desejada
        self.update_service = update_service()

        # Busca e retorna o registro de censec desejado
        return {
            'message': 'Registro de censec atualizado com sucesso',
            'data': self.update_service.execute(censec_id, censec_schema)
        }
    
    # Exclui um registro de censec
    def delete(self, censec_schema: TCensecIdSchema):

        #Importação da classe desejada
        delete_service = self.dynamic_import.service('t_censec_delete_service', 'DeleteService')

        # Instância da classe desejada
        self.delete_service = delete_service()

        # Busca e retorna o registro de censec desejado
        return {
            'message': 'Registro de censec removido com sucesso',
            'data': self.delete_service.execute(censec_schema)
        }