from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.g_tb_regimecomunhao_schema import (
    GTbRegimecomunhaoSaveSchema,
    GTbRegimecomunhaoUpdateSchema,
    GTbRegimecomunhaoIdSchema,
    GTbRegimecomunhaoDescricaoSchema
)


class GTbRegimecomunhaoController:

    def __init__(self):
        # Action responsável por carregar as services de acordo com o estado
        self.dynamic_import = DynamicImport()

        # Define o pacote que deve ser carregado
        self.dynamic_import.set_package("administrativo")

        # Define a tabela que o pacote pertence
        self.dynamic_import.set_table("g_tb_regimecomunhao")
        pass

    # Lista todos os regimes de comunhão
    def index(self):

        # Importação da classe desejada
        indexService = self.dynamic_import.service("g_tb_regimecomunhao_index_service", "IndexService")

        # Instância da classe service
        self.indexService = indexService()

        # Lista todos os regimes de comunhão
        return {
            'message': 'Regimes de comunhão localizados com sucesso',
            'data': self.indexService.execute()
        }


    # Busca um regime de comunhão específico pelo ID
    def show(self, regimecomunhao_schema: GTbRegimecomunhaoIdSchema):

        # Importação da classe desejada
        show_service = self.dynamic_import.service('g_tb_regimecomunhao_show_service', 'ShowService')

        # Instância da classe desejada
        self.show_service = show_service()

        # Busca e retorna o regime de comunhão desejado
        return {
            'message': 'Regime de comunhão localizado com sucesso',
            'data': self.show_service.execute(regimecomunhao_schema)
        }


    # Busca um regime de comunhão pela descrição
    def get_by_descricao(self, regimecomunhao_schema: GTbRegimecomunhaoDescricaoSchema):

        # Importação da classe desejada
        show_service = self.dynamic_import.service('g_tb_regimecomunhao_get_by_descricao_service', 'GetByDescricaoService')

        # Instância da classe desejada
        self.show_service = show_service()

        # Busca e retorna o regime de comunhão desejado
        return {
            'message': 'Regime de comunhão localizado com sucesso',
            'data': self.show_service.execute(regimecomunhao_schema, True)# True para retornar a mensagem de erro caso não localize o serviço
        }


    # Cadastra um novo regime de comunhão
    def save(self, regimecomunhao_schema: GTbRegimecomunhaoSaveSchema):

        # Importação da classe desejada
        save_service = self.dynamic_import.service('g_tb_regimecomunhao_save_service', 'GTbRegimecomunhaoSaveService')

        # Instância da classe desejada
        self.save_service = save_service()

        # Busca e retorna o regime de comunhão desejado
        return {
            'message': 'Regime de comunhão salvo com sucesso',
            'data': self.save_service.execute(regimecomunhao_schema)
        }


    # Atualiza os dados de um regime de comunhão
    def update(self, tb_regimecomunhao_id: int, regimecomunhao_schema: GTbRegimecomunhaoUpdateSchema):

        # Importação da classe desejada
        update_service = self.dynamic_import.service('g_tb_regimecomunhao_update_service', 'GTbRegimecomunhaoUpdateService')

        # Instância da classe desejada
        self.update_service = update_service()

        # Busca e retorna o regime de comunhão desejado
        return {
            'message': 'Regime de comunhão atualizado com sucesso',
            'data': self.update_service.execute(tb_regimecomunhao_id, regimecomunhao_schema)
        }


    # Exclui um regime de comunhão
    def delete(self, regimecomunhao_schema: GTbRegimecomunhaoIdSchema):

        # Importação da classe desejada
        delete_service = self.dynamic_import.service('g_tb_regimecomunhao_delete_service', 'DeleteService')

        # Instância da classe desejada
        self.delete_service = delete_service()

        # Busca e retorna o regime de comunhão desejado
        return {
            'message': 'Regime de comunhão removido com sucesso',
            'data': self.delete_service.execute(regimecomunhao_schema)
        }