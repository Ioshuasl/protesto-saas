from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.g_tb_bairro_schema import (
    GTbBairroSaveSchema,
    GTbBairroUpdateSchema,
    GTbBairroIdSchema,
    GTbBairroDescricaoSchema
)


class GTbBairroController:

    def __init__(self):
        # Action responsável por carregar as services de acordo com o estado
        self.dynamic_import = DynamicImport()

        # Define o pacote que deve ser carregado
        self.dynamic_import.set_package("administrativo")

        # Define a tabela que o pacote pertence
        self.dynamic_import.set_table("g_tb_bairro")
        pass

    # Lista todos os registros de g_tb_bairro
    def index(self):
        
        # Importação da classe desejada
        indexService = self.dynamic_import.service("g_tb_bairro_index_service", "IndexService")

        # Instância da classe service
        self.indexService = indexService()

        # Lista todos os registros de g_tb_bairro
        return {
            'message': 'Registros de bairro localizados com sucesso',
            'data': self.indexService.execute()
        }
    
    
    # Busca um registro de g_tb_bairro específico pelo ID
    def show(self, bairro_schema: GTbBairroIdSchema):

        #Importação da classe desejada
        show_service = self.dynamic_import.service('g_tb_bairro_show_service', 'ShowService')

        # Instância da classe desejada
        self.show_service = show_service()

        # Busca e retorna o registro de g_tb_bairro desejado
        return {
            'message': 'Registro de bairro localizado com sucesso',
            'data': self.show_service.execute(bairro_schema)
        }
    

    # Busca um registro de g_tb_bairro pela descrição
    def get_by_descricao(self, bairro_schema: GTbBairroDescricaoSchema):

        #Importação da classe desejada
        show_service = self.dynamic_import.service('g_tb_bairro_get_descricao_service', 'GetByDescricaoService')

        # Instância da classe desejada
        self.show_service = show_service()

        # Busca e retorna o registro de g_tb_bairro desejado
        return {
            'message': 'Registro de bairro localizado com sucesso',
            'data': self.show_service.execute(bairro_schema, True)
        }  
              
    
    # Cadastra um novo registro de g_tb_bairro
    def save(self, bairro_schema: GTbBairroSaveSchema):

        #Importação da classe desejada
        save_service = self.dynamic_import.service('g_tb_bairro_save_service', 'SaveService')

        # Instância da classe desejada
        self.save_service = save_service()
        # Busca e retorna o registro de g_tb_bairro desejado
        return {
            'message': 'Registro de bairro salvo com sucesso',
            'data': self.save_service.execute(bairro_schema)
        }
    
    # Atualiza os dados de um registro de g_tb_bairro
    def update(self, tb_bairro_id: int, bairro_schema: GTbBairroUpdateSchema):

        #Importação da classe desejada
        update_service = self.dynamic_import.service('g_tb_bairro_update_service', 'UpdateService')

        # Instância da classe desejada
        self.update_service = update_service()

        # Busca e retorna o registro de g_tb_bairro desejado
        return {
            'message': 'Registro de bairro atualizado com sucesso',
            'data': self.update_service.execute(tb_bairro_id, bairro_schema)
        }
    
    # Exclui um registro de g_tb_bairro
    def delete(self, bairro_schema: GTbBairroIdSchema):

        #Importação da classe desejada
        delete_service = self.dynamic_import.service('g_tb_bairro_delete_service', 'DeleteService')

        # Instância da classe desejada
        self.delete_service = delete_service()

        # Busca e retorna o registro de g_tb_bairro desejado
        return {
            'message': 'Registro de bairro removido com sucesso',
            'data': self.delete_service.execute(bairro_schema)
        }