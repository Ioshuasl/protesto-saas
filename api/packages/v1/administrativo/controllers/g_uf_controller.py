from actions.dynamic_import.dynamic_import import DynamicImport

class GUfController:

    def __init__(self):
        # Action responsável por carregar as services de acordo com o estado
        self.dynamic_import = DynamicImport()

        # Define o pacote que deve ser carregado
        self.dynamic_import.set_package("administrativo")

        # Define a tabela que o pacote pertence
        self.dynamic_import.set_table("g_uf")
        pass

    # Lista todos os registros de g_uf
    def index(self):
        
        # Importação da classe desejada
        indexService = self.dynamic_import.service("g_uf_index_service", "IndexService")

        # Instância da classe service
        self.indexService = indexService()

        # Lista todos os registros de g_uf
        return {
            'message': 'Registros de g_uf localizados com sucesso',
            'data': self.indexService.execute()
        }    