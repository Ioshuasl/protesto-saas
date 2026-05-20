from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.g_tb_txmodelogrupo_schema import (
    GTbTxmodelogrupoSaveSchema,
    GTbTxmodelogrupoUpdateSchema,
    GTbTxmodelogrupoIdSchema,
    GTbTxmodelogrupoDescricaoSchema
)


class GTbTxmodelogrupoController:

    def __init__(self):
        # Action responsável por carregar as services de acordo com o estado
        self.dynamic_import = DynamicImport()

        # Define o pacote que deve ser carregado
        self.dynamic_import.set_package("administrativo")

        # Define a tabela que o pacote pertence
        self.dynamic_import.set_table("g_tb_txmodelogrupo")
        pass

    # Lista todos os grupos de modelo de texto
    def index(self):

        # Importação da classe desejada
        index_service = self.dynamic_import.service("g_tb_txmodelogrupo_index_service", "IndexService")

        # Instância da classe service
        self.index_service = index_service()

        # Lista todos os grupos de modelo de texto
        return {
            'message': 'Grupos de modelo de texto localizados com sucesso',
            'data': self.index_service.execute()
        }

    # Busca um grupo de modelo de texto específico pelo ID
    def show(self, txmodelogrupo_schema: GTbTxmodelogrupoIdSchema):

        # Importação da classe desejada
        show_service = self.dynamic_import.service('g_tb_txmodelogrupo_show_service', 'ShowService')

        # Instância da classe desejada
        self.show_service = show_service()

        # Busca e retorna o grupo de modelo de texto desejado
        return {
            'message': 'Grupo de modelo de texto localizado com sucesso',
            'data': self.show_service.execute(txmodelogrupo_schema)
        }

    # Busca um grupo de modelo de texto pela descrição
    def get_by_descricao(self, txmodelogrupo_schema: GTbTxmodelogrupoDescricaoSchema):

        # Importação da classe desejada
        show_service = self.dynamic_import.service('g_tb_txmodelogrupo_get_by_descricao_service', 'GetByDescricaoService')

        # Instância da classe desejada
        self.show_service = show_service()

        # Busca e retorna o grupo de modelo de texto desejado
        return {
            'message': 'Grupo de modelo de texto localizado com sucesso',
            'data': self.show_service.execute(txmodelogrupo_schema, True) # True para retornar a mensagem de erro caso não localize o serviço
        }

    # Cadastra um novo grupo de modelo de texto
    def save(self, txmodelogrupo_schema: GTbTxmodelogrupoSaveSchema):

        # Importação da classe desejada
        save_service = self.dynamic_import.service('g_tb_txmodelogrupo_save_service', 'GTbTxmodelogrupoSaveService')

        # Instância da classe desejada
        self.save_service = save_service()

        # Busca e retorna o grupo de modelo de texto desejado
        return {
            'message': 'Grupo de modelo de texto salvo com sucesso',
            'data': self.save_service.execute(txmodelogrupo_schema)
        }

    # Atualiza os dados de um grupo de modelo de texto
    def update(self, tb_txmodelogrupo_id: int, txmodelogrupo_schema: GTbTxmodelogrupoUpdateSchema):

        # Importação da classe desejada
        update_service = self.dynamic_import.service('g_tb_txmodelogrupo_update_service', 'GTbTxmodelogrupoUpdateService')

        # Instância da classe desejada
        self.update_service = update_service()

        # Busca e retorna o grupo de modelo de texto desejado
        return {
            'message': 'Grupo de modelo de texto atualizado com sucesso',
            'data': self.update_service.execute(tb_txmodelogrupo_id, txmodelogrupo_schema)
        }

    # Exclui um grupo de modelo de texto
    def delete(self, txmodelogrupo_schema: GTbTxmodelogrupoIdSchema):

        # Importação da classe desejada
        delete_service = self.dynamic_import.service('g_tb_txmodelogrupo_delete_service', 'DeleteService')

        # Instância da classe desejada
        self.delete_service = delete_service()

        # Busca e retorna o grupo de modelo de texto desejado
        return {
            'message': 'Grupo de modelo de texto removido com sucesso',
            'data': self.delete_service.execute(txmodelogrupo_schema)
        }