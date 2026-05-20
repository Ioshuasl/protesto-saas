from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.t_imovel_unidade_schema import (
    TImovelUnidadeIndexSchema,
    TImovelUnidadeSaveSchema,
    TImovelUnidadeUpdateSchema,
    TImovelUnidadeIdSchema,
)


class TImovelUnidadeController:

    def __init__(self):
        # Action responsável por carregar as services de acordo com o estado
        self.dynamic_import = DynamicImport()

        # Define o pacote que deve ser carregado
        self.dynamic_import.set_package("administrativo")

        # Define a tabela que o pacote pertence
        self.dynamic_import.set_table("t_imovel_unidade")
        pass

    # Lista todos os registros de imovel_unidade
    def all(self):

        # Importação da classe desejada
        t_imovel_all_service = self.dynamic_import.service(
            "t_imovel_unidade_all_service", "TImovelUnidadeAllService"
        )

        # Instância da classe service
        self.t_imovel_index_service = t_imovel_all_service()

        # Lista todos os registros de imovel_unidade
        return {
            "message": "Registros de t_imovel_unidade localizados com sucesso",
            "data": self.t_imovel_index_service.execute(),
        }

    # Lista todos os registros de imovel_unidade
    def index(self, t_imovel_unidade_index_schema: TImovelUnidadeIndexSchema):

        # Importação da classe desejada
        t_imovel_index_service = self.dynamic_import.service(
            "t_imovel_unidade_index_service", "TImovelUnidadeIndexService"
        )

        # Instância da classe service
        self.t_imovel_index_service = t_imovel_index_service()

        # Lista todos os registros de imovel_unidade
        return {
            "message": "Registros de t_imovel_unidade localizados com sucesso",
            "data": self.t_imovel_index_service.execute(t_imovel_unidade_index_schema),
        }

    # Busca um registro de imovel_unidade específico pelo ID
    def show(self, t_imovel_unidade_id_schema: TImovelUnidadeIdSchema):

        # Importação da classe desejada
        t_imovel_unidade_show_service = self.dynamic_import.service(
            "t_imovel_unidade_show_service", "TImovelUnidadeShowService"
        )

        # Instância da classe desejada
        self.t_imovel_unidade_show_service = t_imovel_unidade_show_service()

        # Busca e retorna o registro de imovel_unidade desejado
        return {
            "message": "Registro de imovel_unidade localizado com sucesso",
            "data": self.t_imovel_unidade_show_service.execute(
                t_imovel_unidade_id_schema
            ),
        }

    # Cadastra um novo registro de imovel_unidade
    def save(self, t_imovel_unidade_save_schema: TImovelUnidadeSaveSchema):

        # Importação da classe desejada
        t_imovel_unidade_save_service = self.dynamic_import.service(
            "t_imovel_unidade_save_service", "TImovelUnidadeSaveService"
        )

        # Instância da classe desejada
        self.t_imovel_unidade_save_service = t_imovel_unidade_save_service()

        # Busca e retorna o registro de imovel_unidade desejado
        return {
            "message": "Registro de imovel_unidade salvo com sucesso",
            "data": self.t_imovel_unidade_save_service.execute(
                t_imovel_unidade_save_schema
            ),
        }

    # Atualiza os dados de um registro de imovel_unidade
    def update(self, t_imovel_unidade_update_schema: TImovelUnidadeUpdateSchema):

        # Importação da classe desejada
        t_imovel_unidade_update_service = self.dynamic_import.service(
            "t_imovel_unidade_update_service", "TImovelUnidadeUpdateService"
        )

        # Instância da classe desejada
        self.t_imovel_unidade_update_service = t_imovel_unidade_update_service()

        # Busca e retorna o registro de imovel_unidade desejado
        return {
            "message": "Registro de imovel_unidade atualizado com sucesso",
            "data": self.t_imovel_unidade_update_service.execute(
                t_imovel_unidade_update_schema
            ),
        }

    # Exclui um registro de imovel_unidade
    def delete(self, t_imovel_unidade_id_schema: TImovelUnidadeIdSchema):

        # Importação da classe desejada
        t_imovel_unidade_delete_service = self.dynamic_import.service(
            "t_imovel_unidade_delete_service", "TImovelUnidadeDeleteService"
        )

        # Instância da classe desejada
        self.t_imovel_unidade_delete_service = t_imovel_unidade_delete_service()

        # Busca e retorna o registro de imovel_unidade desejado
        return {
            "message": "Registro de imovel_unidade removido com sucesso",
            "data": self.t_imovel_unidade_delete_service.execute(
                t_imovel_unidade_id_schema
            ),
        }
