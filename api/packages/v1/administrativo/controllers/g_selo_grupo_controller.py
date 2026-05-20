from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.g_selo_grupo_schema import (
    GSeloGrupoSaveSchema,
    GSeloGrupoUpdateSchema,
    GSeloGrupoIdSchema
)


class GSeloGrupoController:
    """
    Controller responsável por orquestrar as operações CRUD da tabela G_SELO_GRUPO,
    utilizando carregamento dinâmico de serviços via DynamicImport.
    """

    def __init__(self):
        # ----------------------------------------------------
        # Inicialização do DynamicImport
        # ----------------------------------------------------
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("administrativo")
        self.dynamic_import.set_table("g_selo_grupo")

    # ----------------------------------------------------
    # Lista todos os registros de G_SELO_GRUPO
    # ----------------------------------------------------
    def index(self):
        # Importação da classe desejada
        index_service = self.dynamic_import.service("g_selo_grupo_index_service", "GSeloGrupoIndexService")

        # Instância da classe service
        self.index_service = index_service()

        # Execução da listagem
        return {
            "message": "Registros de G_SELO_GRUPO localizados com sucesso.",
            "data": self.index_service.execute(),
        }

    # ----------------------------------------------------
    # Busca um registro específico de G_SELO_GRUPO pelo ID
    # ----------------------------------------------------
    def show(self, g_selo_grupo_id_schema: GSeloGrupoIdSchema):
        # Importação da classe desejada
        show_service = self.dynamic_import.service("g_selo_grupo_show_service", "GSeloGrupoShowService")

        # Instância da classe service
        self.show_service = show_service()

        # Execução da busca
        return {
            "message": "Registro de G_SELO_GRUPO localizado com sucesso.",
            "data": self.show_service.execute(g_selo_grupo_id_schema),
        }

    # ----------------------------------------------------
    # Cadastra um novo registro em G_SELO_GRUPO
    # ----------------------------------------------------
    def save(self, g_selo_grupo_save_schema: GSeloGrupoSaveSchema):
        # Importação da classe desejada
        save_service = self.dynamic_import.service("g_selo_grupo_save_service", "GSeloGrupoSaveService")

        # Instância da classe service
        self.save_service = save_service()

        # Execução do salvamento
        return {
            "message": "Registro de G_SELO_GRUPO salvo com sucesso.",
            "data": self.save_service.execute(g_selo_grupo_save_schema),
        }

    # ----------------------------------------------------
    # Atualiza um registro existente de G_SELO_GRUPO
    # ----------------------------------------------------
    def update(self, g_selo_grupo_update_schema: GSeloGrupoUpdateSchema):
        # Importação da classe desejada
        update_service = self.dynamic_import.service("g_selo_grupo_update_service", "GSeloGrupoUpdateService")

        # Instância da classe service
        self.update_service = update_service()

        # Execução da atualização
        return {
            "message": "Registro de G_SELO_GRUPO atualizado com sucesso.",
            "data": self.update_service.execute(g_selo_grupo_update_schema),
        }

    # ----------------------------------------------------
    # Exclui um registro de G_SELO_GRUPO
    # ----------------------------------------------------
    def delete(self, g_selo_grupo_id_schema: GSeloGrupoIdSchema):
        # Importação da classe desejada
        delete_service = self.dynamic_import.service("g_selo_grupo_delete_service", "GSeloGrupoDeleteService")

        # Instância da classe service
        self.delete_service = delete_service()

        # Execução da exclusão
        return {
            "message": "Registro de G_SELO_GRUPO removido com sucesso.",
            "data": self.delete_service.execute(g_selo_grupo_id_schema),
        }
