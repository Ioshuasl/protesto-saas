from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.g_tb_tipologradouro_schema import (
    GTbTipoLogradouroSaveSchema,
    GTbTipoLogradouroUpdateSchema,
    GTbTipoLogradouroIdSchema,
    GTbTipoLogradouroDescricaoSchema
)

class GTbTipologradouroController:

    def __init__(self):
        # Action responsável por carregar as services de acordo com o estado
        self.dynamic_import = DynamicImport()

        # Define o pacote que deve ser carregado
        self.dynamic_import.set_package("administrativo")

        # Define a tabela que o pacote pertence
        self.dynamic_import.set_table("g_tb_tipologradouro")
        pass

    # Lista todos os registros de tipologradouro
    def index(self):
        
        # Importação da classe desejada
        index_service = self.dynamic_import.service("g_tb_tipologradouro_index_service", "IndexService")

        # Instância da classe service
        self.index_service = index_service()

        # Lista todos os registros de tipologradouro
        return {
            'message': 'Registros de tipologradouro localizados com sucesso',
            'data': self.index_service.execute()
        }
    
    
    # Busca um registro de tipologradouro específico pelo ID
    def show(self, tipologradouro_schema: GTbTipoLogradouroIdSchema):

        #Importação da classe desejada
        show_service = self.dynamic_import.service('g_tb_tipologradouro_show_service', 'ShowService')

        # Instância da classe desejada
        self.show_service = show_service()

        # Busca e retorna o registro de tipologradouro desejado
        return {
            'message': 'Registro de tipologradouro localizado com sucesso',
            'data': self.show_service.execute(tipologradouro_schema)
        }
    

    # Busca um registro de tipologradouro pela descrição
    def get_by_descricao(self, tipologradouro_schema: GTbTipoLogradouroDescricaoSchema):

        #Importação da classe desejada
        show_service = self.dynamic_import.service('g_tb_tipologradouro_get_descricao_service', 'GetByDescricaoService')

        # Instância da classe desejada
        self.show_service = show_service()

        # Busca e retorna o registro de tipologradouro desejado
        return {
            'message': 'Registro de tipologradouro localizado com sucesso',
            'data': self.show_service.execute(tipologradouro_schema, True)
        }  
              
    
    # Cadastra um novo registro de tipologradouro
    def save(self, tipologradouro_schema: GTbTipoLogradouroSaveSchema):

        #Importação da classe desejada
        save_service = self.dynamic_import.service('g_tb_tipologradouro_save_service', 'SaveService')

        # Instância da classe desejada
        self.save_service = save_service()
        # Busca e retorna o registro de tipologradouro desejado
        return {
            'message': 'Registro de tipologradouro salvo com sucesso',
            'data': self.save_service.execute(tipologradouro_schema)
        }
    
    # Atualiza os dados de um registro de tipologradouro
    def update(self, tipologradouro_id: int, tipologradouro_schema: GTbTipoLogradouroUpdateSchema):

        #Importação da classe desejada
        update_service = self.dynamic_import.service('g_tb_tipologradouro_update_service', 'UpdateService')

        # Instância da classe desejada
        self.update_service = update_service()

        # Busca e retorna o registro de tipologradouro desejado
        return {
            'message': 'Registro de tipologradouro atualizado com sucesso',
            'data': self.update_service.execute(tipologradouro_id, tipologradouro_schema)
        }
    
    # Exclui um registro de tipologradouro
    def delete(self, tipologradouro_schema: GTbTipoLogradouroIdSchema):

        #Importação da classe desejada
        delete_service = self.dynamic_import.service('g_tb_tipologradouro_delete_service', 'DeleteService')

        # Instância da classe desejada
        self.delete_service = delete_service()

        # Busca e retorna o registro de tipologradouro desejado
        return {
            'message': 'Registro de tipologradouro removido com sucesso',
            'data': self.delete_service.execute(tipologradouro_schema)
        }