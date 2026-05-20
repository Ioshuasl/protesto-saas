from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.g_tb_documentotipo_schema import (
    GTbDocumentoTipoSaveSchema,
    GTbDocumentoTipoUpdateSchema,
    GTbDocumentoTipoIdSchema,
    GTbDocumentoTipoDescricaoSchema
)

class GTbDocumentoTipoController:

    def __init__(self):
        # Action responsável por carregar as services de acordo com o estado
        self.dynamic_import = DynamicImport()

        # Define o pacote que deve ser carregado
        self.dynamic_import.set_package("administrativo")

        # Define a tabela que o pacote pertence
        self.dynamic_import.set_table("g_tb_documentotipo")
        pass

    # Lista todos os registros de documento_tipo
    def index(self):
        
        # Importação da classe desejada
        indexService = self.dynamic_import.service("g_tb_documentotipo_index_service", "IndexService")

        # Instância da classe service
        self.indexService = indexService()

        # Lista todos os registros de documento_tipo
        return {
            'message': 'Registros de documento_tipo localizados com sucesso',
            'data': self.indexService.execute()
        }
    
    
    # Busca um registro de documento_tipo específico pelo ID
    def show(self, documento_tipo_schema: GTbDocumentoTipoIdSchema):

        #Importação da classe desejada
        show_service = self.dynamic_import.service('g_tb_documentotipo_show_service', 'ShowService')

        # Instância da classe desejada
        self.show_service = show_service()

        # Busca e retorna o registro de documento_tipo desejado
        return {
            'message': 'Registro de documento_tipo localizado com sucesso',
            'data': self.show_service.execute(documento_tipo_schema)
        }
    

    # Busca um registro de documento_tipo pela descrição
    def get_by_descricao(self, documento_tipo_schema: GTbDocumentoTipoDescricaoSchema):

        #Importação da classe desejada
        show_service = self.dynamic_import.service('g_tb_documentotipo_get_by_descricao_service', 'GetByDescricaoService')

        # Instância da classe desejada
        self.show_service = show_service()

        # Busca e retorna o registro de documento_tipo desejado
        return {
            'message': 'Registro de documento_tipo localizado com sucesso',
            'data': self.show_service.execute(documento_tipo_schema, True)
        }  
              
    
    # Cadastra um novo registro de documento_tipo
    def save(self, documento_tipo_schema: GTbDocumentoTipoSaveSchema):

        #Importação da classe desejada
        save_service = self.dynamic_import.service('g_tb_documentotipo_save_service', 'SaveService')

        # Instância da classe desejada
        self.save_service = save_service()
        # Busca e retorna o registro de documento_tipo desejado
        return {
            'message': 'Registro de documento_tipo salvo com sucesso',
            'data': self.save_service.execute(documento_tipo_schema)
        }
    
    # Atualiza os dados de um registro de documento_tipo
    def update(self, documento_tipo_id: int, documento_tipo_schema: GTbDocumentoTipoUpdateSchema):

        #Importação da classe desejada
        update_service = self.dynamic_import.service('g_tb_documentotipo_update_service', 'UpdateService')

        # Instância da classe desejada
        self.update_service = update_service()

        # Busca e retorna o registro de documento_tipo desejado
        return {
            'message': 'Registro de documento_tipo atualizado com sucesso',
            'data': self.update_service.execute(documento_tipo_id, documento_tipo_schema)
        }
    
    # Exclui um registro de documento_tipo
    def delete(self, documento_tipo_schema: GTbDocumentoTipoIdSchema):

        #Importação da classe desejada
        delete_service = self.dynamic_import.service('g_tb_documentotipo_delete_service', 'DeleteService')

        # Instância da classe desejada
        self.delete_service = delete_service()

        # Busca e retorna o registro de documento_tipo desejado
        return {
            'message': 'Registro de documento_tipo removido com sucesso',
            'data': self.delete_service.execute(documento_tipo_schema)
        }