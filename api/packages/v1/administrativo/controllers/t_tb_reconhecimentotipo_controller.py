from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.t_tb_reconhecimentotipo_schema import (
    TTbReconhecimentotipoSaveSchema,
    TTbReconhecimentotipoUpdateSchema,
    TTbReconhecimentotipoIdSchema,
    TTbReconhecimentotipoDescricaoSchema
)

class TTbReconhecimentotipoController:

    def __init__(self):
        # Action responsável por carregar as services de acordo com o estado
        self.dynamic_import = DynamicImport()

        # Define o pacote que deve ser carregado
        self.dynamic_import.set_package("administrativo")

        # Define a tabela que o pacote pertence
        self.dynamic_import.set_table("t_tb_reconhecimentotipo")
        pass

    # Lista todos os tipos de reconhecimento
    def index(self):
        
        # Importação da classe desejada
        indexService = self.dynamic_import.service("t_tb_reconhecimentotipo_index_service", "IndexService")

        # Instância da classe service
        self.indexService = indexService()

        # Lista todos os tipos de reconhecimento
        return {
            'message': 'Tipos de reconhecimento localizados com sucesso',
            'data': self.indexService.execute()
        }
    
    
    # Busca um tipo de reconhecimento específico pelo ID
    def show(self, reconhecimentotipo_schema : TTbReconhecimentotipoIdSchema):

        #Importação da classe desejada
        show_service = self.dynamic_import.service('t_tb_reconhecimentotipo_show_service', 'ShowService')

        # Instância da classe desejada
        self.show_service = show_service()

        # Busca e retorna o tipo de reconhecimento desejado
        return {
            'message' : 'Tipo de reconhecimento localizado com sucesso',
            'data': self.show_service.execute(reconhecimentotipo_schema)
        }
    

    # Busca um tipo de reconhecimento pela descrição
    def get_by_descricao(self, reconhecimentotipo_schema : TTbReconhecimentotipoDescricaoSchema):

        #Importação da classe desejada
        show_service = self.dynamic_import.service('t_tb_reconhecimentotipo_get_descricao_service', 'GetByDescricaoService')

        # Instância da classe desejada
        self.show_service = show_service()

        # Busca e retorna o tipo de reconhecimento desejado
        return {
            'message' : 'Tipo de reconhecimento localizado com sucesso',
            'data': self.show_service.execute(reconhecimentotipo_schema, True) #True para retornar a mensagem de erro caso não localize o serviço
        }  
              
    
    # Cadastra um novo tipo de reconhecimento
    def save(self, reconhecimentotipo_schema : TTbReconhecimentotipoSaveSchema):

        #Importação da classe desejada
        save_service = self.dynamic_import.service('t_tb_reconhecimentotipo_save_service', 'TTbReconhecimentotipoSaveService')

        # Instância da classe desejada
        self.save_service = save_service()
        # Busca e retorna o tipo de reconhecimento desejado
        return {
            'message' : 'Tipo de reconhecimento salvo com sucesso',
            'data': self.save_service.execute(reconhecimentotipo_schema)
        }
    
    # Atualiza os dados de um tipo de reconhecimento
    def update(self, tb_reconhecimentotipo_id : int, reconhecimentotipo_schema : TTbReconhecimentotipoUpdateSchema):

        #Importação da classe desejada
        update_service = self.dynamic_import.service('t_tb_reconhecimentotipo_update_service', 'TTbReconhecimentotipoUpdateService')

        # Instância da classe desejada
        self.update_service = update_service()

        # Busca e retorna o tipo de reconhecimento desejado
        return {
            'message' : 'Tipo de reconhecimento atualizado com sucesso',
            'data': self.update_service.execute(tb_reconhecimentotipo_id, reconhecimentotipo_schema)
        }
    
    # Exclui um tipo de reconhecimento
    def delete(self, reconhecimentotipo_schema : TTbReconhecimentotipoIdSchema):

        #Importação da classe desejada
        delete_service = self.dynamic_import.service('t_tb_reconhecimentotipo_delete_service', 'DeleteService')

        # Instância da classe desejada
        self.delete_service = delete_service()

        # Busca e retorna o tipo de reconhecimento desejado
        return {
            'message' : 'Tipo de reconhecimento removido com sucesso',
            'data': self.delete_service.execute(reconhecimentotipo_schema)
        }
