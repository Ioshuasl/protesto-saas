from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.t_censec_qualidade_schema import (
    TCensecQualidadeSaveSchema,
    TCensecQualidadeUpdateSchema,
    TCensecQualidadeIdSchema,
    TCensecQualidadeDescricaoSchema
)

class TCensecQualidadeController:

    def __init__(self):
        # Action responsável por carregar as services de acordo com o estado
        self.dynamic_import = DynamicImport()

        # Define o pacote que deve ser carregado
        self.dynamic_import.set_package("administrativo")

        # Define a tabela que o pacote pertence
        self.dynamic_import.set_table("t_censec_qualidade")
        pass

    # Lista todos os registros de censec_qualidade
    def index(self):
        
        # Importação da classe desejada
        indexService = self.dynamic_import.service("t_censec_qualidade_index_service", "IndexService")

        # Instância da classe service
        self.indexService = indexService()

        # Lista todos os registros de censec_qualidade
        return {
            'message': 'Registros de censec_qualidade localizados com sucesso',
            'data': self.indexService.execute()
        }
    
    
    # Busca um registro de censec_qualidade específico pelo ID
    def show(self, censec_qualidade_schema: TCensecQualidadeIdSchema):

        #Importação da classe desejada
        show_service = self.dynamic_import.service('t_censec_qualidade_show_service', 'ShowService')

        # Instância da classe desejada
        self.show_service = show_service()

        # Busca e retorna o registro de censec_qualidade desejado
        return {
            'message': 'Registro de censec_qualidade localizado com sucesso',
            'data': self.show_service.execute(censec_qualidade_schema)
        }
    

    # Busca um registro de censec_qualidade pela descrição
    def get_by_descricao(self, censec_qualidade_schema: TCensecQualidadeDescricaoSchema):

        #Importação da classe desejada
        show_service = self.dynamic_import.service('t_censec_qualidade_get_descricao_service', 'GetByDescricaoService')

        # Instância da classe desejada
        self.show_service = show_service()

        # Busca e retorna o registro de censec_qualidade desejado
        return {
            'message': 'Registro de censec_qualidade localizado com sucesso',
            'data': self.show_service.execute(censec_qualidade_schema, True)
        }  
              
    
    # Cadastra um novo registro de censec_qualidade
    def save(self, censec_qualidade_schema: TCensecQualidadeSaveSchema):

        #Importação da classe desejada
        save_service = self.dynamic_import.service('t_censec_qualidade_save_service', 'SaveService')

        # Instância da classe desejada
        self.save_service = save_service()
        # Busca e retorna o registro de censec_qualidade desejado
        return {
            'message': 'Registro de censec_qualidade salvo com sucesso',
            'data': self.save_service.execute(censec_qualidade_schema)
        }
    
    # Atualiza os dados de um registro de censec_qualidade
    def update(self, censec_qualidade_id: int, censec_qualidade_schema: TCensecQualidadeUpdateSchema):

        #Importação da classe desejada
        update_service = self.dynamic_import.service('t_censec_qualidade_update_service', 'UpdateService')

        # Instância da classe desejada
        self.update_service = update_service()

        # Busca e retorna o registro de censec_qualidade desejado
        return {
            'message': 'Registro de censec_qualidade atualizado com sucesso',
            'data': self.update_service.execute(censec_qualidade_id, censec_qualidade_schema)
        }
    
    # Exclui um registro de censec_qualidade
    def delete(self, censec_qualidade_schema: TCensecQualidadeIdSchema):

        #Importação da classe desejada
        delete_service = self.dynamic_import.service('t_censec_qualidade_delete_service', 'DeleteService')

        # Instância da classe desejada
        self.delete_service = delete_service()

        # Busca e retorna o registro de censec_qualidade desejado
        return {
            'message': 'Registro de censec_qualidade removido com sucesso',
            'data': self.delete_service.execute(censec_qualidade_schema)
        }