from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.t_censec_naturezalitigio_schema import (
    TCensecNaturezalitigioSaveSchema,
    TCensecNaturezalitigioUpdateSchema,
    TCensecNaturezalitigioIdSchema,
    TCensecNaturezalitigioDescricaoSchema
)

class TCensecNaturezalitigioController:

    def __init__(self):
        # Action responsável por carregar as services de acordo com o estado
        self.dynamic_import = DynamicImport()

        # Define o pacote que deve ser carregado
        self.dynamic_import.set_package("administrativo")

        # Define a tabela que o pacote pertence
        self.dynamic_import.set_table("t_censec_naturezalitigio")
        pass

    # Lista todos os registros de natureza_litigio
    def index(self):
        
        # Importação da classe desejada
        indexService = self.dynamic_import.service("t_censec_naturezalitigio_index_service", "IndexService")

        # Instância da classe service
        self.indexService = indexService()

        # Lista todos os registros de natureza_litigio
        return {
            'message': 'Registros de natureza_litigio localizados com sucesso',
            'data': self.indexService.execute()
        }
    
    
    # Busca um registro de natureza_litigio específico pelo ID
    def show(self, censec_naturezalitigio_schema: TCensecNaturezalitigioIdSchema):

        #Importação da classe desejada
        show_service = self.dynamic_import.service('t_censec_naturezalitigio_show_service', 'ShowService')

        # Instância da classe desejada
        self.show_service = show_service()

        # Busca e retorna o registro de natureza_litigio desejado
        return {
            'message': 'Registro de natureza_litigio localizado com sucesso',
            'data': self.show_service.execute(censec_naturezalitigio_schema)
        }
    

    # Busca um registro de natureza_litigio pela descrição
    def get_by_descricao(self, censec_naturezalitigio_schema: TCensecNaturezalitigioDescricaoSchema):

        #Importação da classe desejada
        show_service = self.dynamic_import.service('t_censec_naturezalitigio_get_descricao_service', 'GetByDescricaoService')

        # Instância da classe desejada
        self.show_service = show_service()

        # Busca e retorna o registro de natureza_litigio desejado
        return {
            'message': 'Registro de natureza_litigio localizado com sucesso',
            'data': self.show_service.execute(censec_naturezalitigio_schema, True)
        }  
              
    
    # Cadastra um novo registro de natureza_litigio
    def save(self, censec_naturezalitigio_schema: TCensecNaturezalitigioSaveSchema):

        #Importação da classe desejada
        save_service = self.dynamic_import.service('t_censec_naturezalitigio_save_service', 'SaveService')

        # Instância da classe desejada
        self.save_service = save_service()
        # Busca e retorna o registro de natureza_litigio desejado
        return {
            'message': 'Registro de natureza_litigio salvo com sucesso',
            'data': self.save_service.execute(censec_naturezalitigio_schema)
        }
    
    # Atualiza os dados de um registro de natureza_litigio
    def update(self, censec_naturezalitigio_id: int, censec_naturezalitigio_schema: TCensecNaturezalitigioUpdateSchema):

        #Importação da classe desejada
        update_service = self.dynamic_import.service('t_censec_naturezalitigio_update_service', 'UpdateService')

        # Instância da classe desejada
        self.update_service = update_service()

        # Busca e retorna o registro de natureza_litigio desejado
        return {
            'message': 'Registro de natureza_litigio atualizado com sucesso',
            'data': self.update_service.execute(censec_naturezalitigio_id, censec_naturezalitigio_schema)
        }
    
    # Exclui um registro de natureza_litigio
    def delete(self, censec_naturezalitigio_schema: TCensecNaturezalitigioIdSchema):

        #Importação da classe desejada
        delete_service = self.dynamic_import.service('t_censec_naturezalitigio_delete_service', 'DeleteService')

        # Instância da classe desejada
        self.delete_service = delete_service()

        # Busca e retorna o registro de natureza_litigio desejado
        return {
            'message': 'Registro de natureza_litigio removido com sucesso',
            'data': self.delete_service.execute(censec_naturezalitigio_schema)
        }