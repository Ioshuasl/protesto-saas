from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.g_natureza_titulo_schema import (
    GNaturezaTituloIndexSchema,
    GNaturezaTituloSaveSchema,
    GNaturezaTituloUpdateSchema,
    GNaturezaTituloIdSchema
)


class GNaturezaTituloController:
    """
    Controller responsável por orquestrar as operações CRUD da tabela G_NATUREZA_TITULO,
    utilizando carregamento dinâmico de serviços via DynamicImport.
    """

    def __init__(self):
        # ----------------------------------------------------
        # Inicialização do DynamicImport
        # ----------------------------------------------------
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("administrativo")
        self.dynamic_import.set_table("g_natureza_titulo")

    # ----------------------------------------------------
    # Lista todos os registros de G_NATUREZA_TITULO
    # ----------------------------------------------------
    def index(self, g_natureza_titulo_index_schema: GNaturezaTituloIndexSchema):
        # Importação da classe desejada
        index_service = self.dynamic_import.service("g_natureza_titulo_index_service", "GNaturezaTituloIndexService")

        # Instância da classe service
        self.index_service = index_service()

        # Execução da listagem
        return {
            "message": "Registros de G_NATUREZA_TITULO localizados com sucesso.",
            "data": self.index_service.execute(g_natureza_titulo_index_schema),
        }

    # ----------------------------------------------------
    # Busca um registro específico de G_NATUREZA_TITULO pelo ID
    # ----------------------------------------------------
    def show(self, g_natureza_titulo_id_schema: GNaturezaTituloIdSchema):
        # Importação da classe desejada
        show_service = self.dynamic_import.service("g_natureza_titulo_show_service", "GNaturezaTituloShowService")

        # Instância da classe service
        self.show_service = show_service()

        # Execução da busca
        return {
            "message": "Registro de G_NATUREZA_TITULO localizado com sucesso.",
            "data": self.show_service.execute(g_natureza_titulo_id_schema),
        }

    # ----------------------------------------------------
    # Cadastra um novo registro em G_NATUREZA_TITULO
    # ----------------------------------------------------
    def save(self, g_natureza_titulo_save_schema: GNaturezaTituloSaveSchema):
        # Importação da classe desejada
        save_service = self.dynamic_import.service("g_natureza_titulo_save_service", "GNaturezaTituloSaveService")

        # Instância da classe service
        self.save_service = save_service()

        # Execução do salvamento
        return {
            "message": "Registro de G_NATUREZA_TITULO salvo com sucesso.",
            "data": self.save_service.execute(g_natureza_titulo_save_schema),
        }

    # ----------------------------------------------------
    # Atualiza um registro existente de G_NATUREZA_TITULO
    # ----------------------------------------------------
    def update(self, g_natureza_titulo_update_schema: GNaturezaTituloUpdateSchema):
        # Importação da classe desejada
        update_service = self.dynamic_import.service("g_natureza_titulo_update_service", "GNaturezaTituloUpdateService")

        # Instância da classe service
        self.update_service = update_service()

        # Execução da atualização
        return {
            "message": "Registro de G_NATUREZA_TITULO atualizado com sucesso.",
            "data": self.update_service.execute(g_natureza_titulo_update_schema),
        }

    # ----------------------------------------------------
    # Exclui um registro de G_NATUREZA_TITULO
    # ----------------------------------------------------
    def delete(self, g_natureza_titulo_id_schema: GNaturezaTituloIdSchema):
        # Importação da classe desejada
        delete_service = self.dynamic_import.service("g_natureza_titulo_delete_service", "GNaturezaTituloDeleteService")

        # Instância da classe service
        self.delete_service = delete_service()

        # Execução da exclusão
        return {
            "message": "Registro de G_NATUREZA_TITULO removido com sucesso.",
            "data": self.delete_service.execute(g_natureza_titulo_id_schema),
        }
