from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.t_imovel_schema import (
    TImovelIndexSchema,
    TImovelSaveSchema,
    TImovelUpdateSchema,
    TImovelIdSchema
)

class TImovelController:

    def __init__(self):
        # Action responsável por carregar as services de acordo com o estado
        self.dynamic_import = DynamicImport()

        # Define o pacote que deve ser carregado
        self.dynamic_import.set_package("administrativo")

        # Define a tabela que o pacote pertence
        self.dynamic_import.set_table("t_imovel")
        pass

    # Lista todos os registros de t_imovel
    def index(self, t_imovel_index_schema: TImovelIndexSchema):
        
        # Importação da classe desejada
        t_imovel_index_service = self.dynamic_import.service("t_imovel_index_service", "TImovelIndexService")

        # Instância da classe service
        self.t_imovel_index_service = t_imovel_index_service()

        # Lista todos os registros de t_imovel
        return {
            'message': 'Registros de t_imovel localizados com sucesso',
            'data': self.t_imovel_index_service.execute(t_imovel_index_schema)
        }
    
    
    # Busca um registro de t_imovel específico pelo ID
    def show(self, t_imovel_id_schema: TImovelIdSchema):

        #Importação da classe desejada
        show_service = self.dynamic_import.service('t_imovel_show_service', 'TImovelShowService')

        # Instância da classe desejada
        self.show_service = show_service()

        # Busca e retorna o registro de t_imovel desejado
        return {
            'message': 'Registro de t_imovel localizado com sucesso',
            'data': self.show_service.execute(t_imovel_id_schema)
        }
    
    # Cadastra um novo registro de t_imovel
    def save(self, t_imovel_save_schema: TImovelSaveSchema):

        #Importação da classe desejada
        save_service = self.dynamic_import.service('t_imovel_save_service', 'TImovelSaveService')

        # Instância da classe desejada
        self.save_service = save_service()
        # Busca e retorna o registro de t_imovel desejado
        return {
            'message': 'Registro de t_imovel salvo com sucesso',
            'data': self.save_service.execute(t_imovel_save_schema)
        }
    
    # Atualiza os dados de um registro de t_imovel
    def update(self, t_imovel_update_schema: TImovelUpdateSchema):

        #Importação da classe desejada
        update_service = self.dynamic_import.service('t_imovel_update_service', 'TImovelUpdateService')

        # Instância da classe desejada
        self.update_service = update_service()

        # Busca e retorna o registro de t_imovel desejado
        return {
            'message': 'Registro de t_imovel atualizado com sucesso',
            'data': self.update_service.execute(t_imovel_update_schema)
        }
    
    # Exclui um registro de t_imovel
    def delete(self, t_imovel_schema: TImovelIdSchema):

        #Importação da classe desejada
        delete_service = self.dynamic_import.service('t_imovel_delete_service', 'TImovelDeleteService')

        # Instância da classe desejada
        self.delete_service = delete_service()

        # Busca e retorna o registro de t_imovel desejado
        return {
            'message': 'Registro de t_imovel removido com sucesso',
            'data': self.delete_service.execute(t_imovel_schema)
        }