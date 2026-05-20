from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.g_gramatica_schema import (
    GGramaticaSaveSchema,
    GGramaticaUpdateSchema,
    GGramaticaIdSchema,
)


class GGramaticaController:
    """
    Controller responsável por orquestrar as operações CRUD da tabela G_GRAMATICA,
    utilizando carregamento dinâmico de serviços via DynamicImport.
    """

    def __init__(self):
        # ----------------------------------------------------
        # Inicialização do DynamicImport
        # ----------------------------------------------------
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("administrativo")
        self.dynamic_import.set_table("g_gramatica")

    # ----------------------------------------------------
    # Lista todos os registros de G_GRAMATICA
    # ----------------------------------------------------
    def index(self):

        # Importação da classe desejada
        index_service = self.dynamic_import.service(
            "g_gramatica_index_service", "GGramaticaIndexService"
        )

        # Instância da classe service
        self.index_service = index_service()

        # Execução da listagem
        return {
            "message": "Registros de G_GRAMATICA localizados com sucesso.",
            "data": self.index_service.execute(),
        }

    # ----------------------------------------------------
    # Busca um registro específico de G_GRAMATICA pelo ID
    # ----------------------------------------------------
    def show(self, g_gramatica_id_schema: GGramaticaIdSchema):
        # Importação da classe desejada
        show_service = self.dynamic_import.service(
            "g_gramatica_show_service", "GGramaticaShowService"
        )

        # Instância da classe service
        self.show_service = show_service()

        # Execução da busca
        return {
            "message": "Registro de G_GRAMATICA localizado com sucesso.",
            "data": self.show_service.execute(g_gramatica_id_schema),
        }

    # ----------------------------------------------------
    # Cadastra um novo registro em G_GRAMATICA
    # ----------------------------------------------------
    def save(self, g_gramatica_save_schema: GGramaticaSaveSchema):
        # Importação da classe desejada
        save_service = self.dynamic_import.service(
            "g_gramatica_save_service", "GGramaticaSaveService"
        )

        # Instância da classe service
        self.save_service = save_service()

        # Execução do salvamento
        return {
            "message": "Registro de G_GRAMATICA salvo com sucesso.",
            "data": self.save_service.execute(g_gramatica_save_schema),
        }

    # ----------------------------------------------------
    # Atualiza um registro existente de G_GRAMATICA
    # ----------------------------------------------------
    def update(self, g_gramatica_update_schema: GGramaticaUpdateSchema):
        # Importação da classe desejada
        update_service = self.dynamic_import.service(
            "g_gramatica_update_service", "GGramaticaUpdateService"
        )

        # Instância da classe service
        self.update_service = update_service()

        # Execução da atualização
        return {
            "message": "Registro de G_GRAMATICA atualizado com sucesso.",
            "data": self.update_service.execute(g_gramatica_update_schema),
        }

    # ----------------------------------------------------
    # Exclui um registro de G_GRAMATICA
    # ----------------------------------------------------
    def delete(self, g_gramatica_id_schema: GGramaticaIdSchema):
        # Importação da classe desejada
        delete_service = self.dynamic_import.service(
            "g_gramatica_delete_service", "GGramaticaDeleteService"
        )

        # Instância da classe service
        self.delete_service = delete_service()

        # Execução da exclusão
        return {
            "message": "Registro de G_GRAMATICA removido com sucesso.",
            "data": self.delete_service.execute(g_gramatica_id_schema),
        }
