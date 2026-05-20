from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.t_tb_andamentoservico_schema import (
    TTbAndamentoservicoSaveSchema,
    TTbAndamentoservicoUpdateSchema,
    TTbAndamentoservicoIdSchema,
    TTbAndamentoservicoDescricaoSchema
)

class TTbAndamentoservicoController:

    def __init__(self):
        # Action responsável por carregar as services de acordo com o estado
        self.dynamic_import = DynamicImport()

        # Define o pacote que deve ser carregado
        self.dynamic_import.set_package("administrativo")

        # Define a tabela que o pacote pertence
        self.dynamic_import.set_table("t_tb_andamentoservico")
        pass

    # Lista todos os andamentos de serviço
    def index(self):
        
        # Importação da classe desejada
        indexService = self.dynamic_import.service("t_tb_andamentoservico_index_service", "IndexService")

        # Instância da classe service
        self.indexService = indexService()

        # Lista todos os andamentos de serviço
        return {
            'message': 'Andamentos de serviço localizados com sucesso',
            'data': self.indexService.execute()
        }
    
    
    # Busca um andamento de serviço específico pelo ID
    def show(self, andamentoservico_schema : TTbAndamentoservicoIdSchema):

        #Importação da classe desejada
        show_service = self.dynamic_import.service('t_tb_andamentoservico_show_service', 'ShowService')

        # Instância da classe desejada
        self.show_service = show_service()

        # Busca e retorna o andamento de serviço desejado
        return {
            'message' : 'Andamento de serviço localizado com sucesso',
            'data': self.show_service.execute(andamentoservico_schema)
        }
    

    # Busca um andamento de serviço pela descrição
    def get_by_descricao(self, andamentoservico_schema : TTbAndamentoservicoDescricaoSchema):

        #Importação da classe desejada
        show_service = self.dynamic_import.service('t_tb_andamentoservico_get_descricao_service', 'GetByDescricaoService')

        # Instância da classe desejada
        self.show_service = show_service()

        # Busca e retorna o andamento de serviço desejado
        return {
            'message' : 'Andamento de serviço localizado com sucesso',
            'data': self.show_service.execute(andamentoservico_schema, True) #True para retornar a mensagem de erro caso não localize o serviço
        }  
              
    
    # Cadastra um novo andamento de serviço
    def save(self, andamentoservico_schema : TTbAndamentoservicoSaveSchema):

        #Importação da classe desejada
        save_service = self.dynamic_import.service('t_tb_andamentoservico_save_service', 'TTbAndamentoservicoSaveService')

        # Instância da classe desejada
        self.save_service = save_service()
        # Busca e retorna o andamento de serviço desejado
        return {
            'message' : 'Andamento de serviço salvo com sucesso',
            'data': self.save_service.execute(andamentoservico_schema)
        }
    
    # Atualiza os dados de um andamento de serviço
    def update(self, tb_andamentoservico_id : int, andamentoservico_schema : TTbAndamentoservicoUpdateSchema):

        #Importação da classe desejada
        update_service = self.dynamic_import.service('t_tb_andamentoservico_update_service', 'TTbAndamentoservicoUpdateService')

        # Instância da classe desejada
        self.update_service = update_service()

        # Busca e retorna o andamento de serviço desejado
        return {
            'message' : 'Andamento de serviço atualizado com sucesso',
            'data': self.update_service.execute(tb_andamentoservico_id, andamentoservico_schema)
        }
    
    # Exclui um andamento de serviço
    def delete(self, andamentoservico_schema : TTbAndamentoservicoIdSchema):

        #Importação da classe desejada
        delete_service = self.dynamic_import.service('t_tb_andamentoservico_delete_service', 'DeleteService')

        # Instância da classe desejada
        self.delete_service = delete_service()

        # Busca e retorna o andamento de serviço desejado
        return {
            'message' : 'Andamento de serviço removido com sucesso',
            'data': self.delete_service.execute(andamentoservico_schema)
        }