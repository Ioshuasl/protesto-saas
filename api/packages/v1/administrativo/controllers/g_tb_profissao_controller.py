from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.g_tb_profissao_schema import (
    GTbProfissaoSaveSchema,
    GTbProfissaoUpdateSchema,
    GTbProfissaoIdSchema,
    GTbProfissaoDescricaoSchema
)

class GTbProfissaoController:

    def __init__(self):
        # Action responsável por carregar as services de acordo com o estado
        self.dynamic_import = DynamicImport()

        # Define o pacote que deve ser carregado
        self.dynamic_import.set_package("administrativo")

        # Define a tabela que o pacote pertence
        self.dynamic_import.set_table("g_tb_profissao")
        pass

    # Lista todas as profissões
    def index(self):
        
        # Importação da classe desejada
        indexService = self.dynamic_import.service("g_tb_profissao_index_service", "IndexService")

        # Instância da classe service
        self.indexService = indexService()

        # Lista todas as profissões
        return {
            'message': 'Profissões localizadas com sucesso',
            'data': self.indexService.execute()
        }
    
    
    # Busca uma profissão específica pelo ID
    def show(self, profissao_schema: GTbProfissaoIdSchema):

        #Importação da classe desejada
        show_service = self.dynamic_import.service('g_tb_profissao_show_service', 'ShowService')

        # Instância da classe desejada
        self.show_service = show_service()

        # Busca e retorna a profissão desejada
        return {
            'message' : 'Profissão localizada com sucesso',
            'data': self.show_service.execute(profissao_schema)
        }
    

    # Busca uma profissão pela descrição
    def get_by_descricao(self, profissao_schema: GTbProfissaoDescricaoSchema):

        #Importação da classe desejada
        show_service = self.dynamic_import.service('g_tb_profissao_get_descricao_service', 'GetByDescricaoService')

        # Instância da classe desejada
        self.show_service = show_service()

        # Busca e retorna a profissão desejada
        return {
            'message' : 'Profissão localizada com sucesso',
            'data': self.show_service.execute(profissao_schema, True) #True para retornar a mensagem de erro caso não localize o serviço
        }  


    # Busca profissões pela descrição (lista)
    def search_by_descricao(self, profissao_schema: GTbProfissaoDescricaoSchema):

        # Importação da classe desejada
        search_service = self.dynamic_import.service(
            'g_tb_profissao_search_by_descricao_service',
            'SearchByDescricaoService'
        )

        # Instância da classe desejada
        self.search_service = search_service()

        # Busca e retorna as profissões desejadas
        return {
            'message': 'Profissões localizadas com sucesso',
            'data': self.search_service.execute(profissao_schema)
        }
              
    
    # Cadastra uma nova profissão
    def save(self, profissao_schema: GTbProfissaoSaveSchema):

        #Importação da classe desejada
        save_service = self.dynamic_import.service('g_tb_profissao_save_service', 'GTbProfissaoSaveService')

        # Instância da classe desejada
        self.save_service = save_service()
        # Busca e retorna a profissão desejada
        return {
            'message' : 'Profissão salva com sucesso',
            'data': self.save_service.execute(profissao_schema)
        }
    
    # Atualiza os dados de uma profissão
    def update(self, tb_profissao_id: float, profissao_schema: GTbProfissaoUpdateSchema):

        #Importação da classe desejada
        update_service = self.dynamic_import.service('g_tb_profissao_update_service', 'GTbProfissaoUpdateService')

        # Instância da classe desejada
        self.update_service = update_service()

        # Busca e retorna a profissão desejada
        return {
            'message' : 'Profissão atualizada com sucesso',
            'data': self.update_service.execute(tb_profissao_id, profissao_schema)
        }
    
    # Exclui uma profissão
    def delete(self, profissao_schema: GTbProfissaoIdSchema):

        #Importação da classe desejada
        delete_service = self.dynamic_import.service('g_tb_profissao_delete_service', 'DeleteService')

        # Instância da classe desejada
        self.delete_service = delete_service()

        # Busca e retorna a profissão desejada
        return {
            'message' : 'Profissão removida com sucesso',
            'data': self.delete_service.execute(profissao_schema)
        }