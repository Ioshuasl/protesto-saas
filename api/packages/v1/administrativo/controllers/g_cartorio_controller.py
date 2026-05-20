from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.g_cartorio_schema import (
    GCartorioSaveSchema,
    GCartorioUpdateSchema,
    GCartorioIdSchema
)


class GCartorioController:
    """
    Controller responsável por orquestrar as operações CRUD da tabela G_CARTORIO,
    utilizando carregamento dinâmico de serviços via DynamicImport.
    """

    def __init__(self):
        # ----------------------------------------------------
        # Inicialização do DynamicImport
        # ----------------------------------------------------
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("administrativo")
        self.dynamic_import.set_table("g_cartorio")

    # ----------------------------------------------------
    # Lista todos os registros de G_CARTORIO
    # ----------------------------------------------------
    def index(self):
        # Importação da classe desejada
        index_service = self.dynamic_import.service("g_cartorio_index_service", "GCartorioIndexService")

        # Instância da classe service
        self.index_service = index_service()

        # Execução da listagem
        return {
            "message": "Registros de G_CARTORIO localizados com sucesso.",
            "data": self.index_service.execute(),
        }

    # ----------------------------------------------------
    # Busca um registro específico de G_CARTORIO pelo ID
    # ----------------------------------------------------
    def show(self, g_cartorio_id_schema: GCartorioIdSchema):
        # Importação da classe desejada
        show_service = self.dynamic_import.service("g_cartorio_show_service", "GCartorioShowService")

        # Instância da classe service
        self.show_service = show_service()

        # Execução da busca
        return {
            "message": "Registro de G_CARTORIO localizado com sucesso.",
            "data": self.show_service.execute(g_cartorio_id_schema),
        }

    # ----------------------------------------------------
    # Cadastra um novo registro em G_CARTORIO
    # ----------------------------------------------------
    def save(self, g_cartorio_save_schema: GCartorioSaveSchema):
        # Importação da classe desejada
        save_service = self.dynamic_import.service("g_cartorio_save_service", "GCartorioSaveService")

        # Instância da classe service
        self.save_service = save_service()

        # Execução do salvamento
        return {
            "message": "Registro de G_CARTORIO salvo com sucesso.",
            "data": self.save_service.execute(g_cartorio_save_schema),
        }

    # ----------------------------------------------------
    # Atualiza um registro existente de G_CARTORIO
    # ----------------------------------------------------
    def update(self, g_cartorio_update_schema: GCartorioUpdateSchema):
        # Importação da classe desejada
        update_service = self.dynamic_import.service("g_cartorio_update_service", "GCartorioUpdateService")

        # Instância da classe service
        self.update_service = update_service()

        # Execução da atualização
        return {
            "message": "Registro de G_CARTORIO atualizado com sucesso.",
            "data": self.update_service.execute(g_cartorio_update_schema),
        }

    # ----------------------------------------------------
    # Exclui um registro de G_CARTORIO
    # ----------------------------------------------------
    def delete(self, g_cartorio_id_schema: GCartorioIdSchema):
        # Importação da classe desejada
        delete_service = self.dynamic_import.service("g_cartorio_delete_service", "GCartorioDeleteService")

        # Instância da classe service
        self.delete_service = delete_service()

        # Execução da exclusão
        return {
            "message": "Registro de G_CARTORIO removido com sucesso.",
            "data": self.delete_service.execute(g_cartorio_id_schema),
        }
