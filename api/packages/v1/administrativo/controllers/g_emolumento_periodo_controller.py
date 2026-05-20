from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.g_emolumento_periodo_schema import (
    GEmolumentoPeriodoSaveSchema,
    GEmolumentoPeriodoUpdateSchema,
    GEmolumentoPeriodoIdSchema
)


class GEmolumentoPeriodoController:
    """
    Controller responsável por orquestrar as operações CRUD da tabela G_EMOLUMENTO_PERIODO,
    utilizando carregamento dinâmico de serviços via DynamicImport.
    """

    def __init__(self):
        # ----------------------------------------------------
        # Inicialização do DynamicImport
        # ----------------------------------------------------
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("administrativo")
        self.dynamic_import.set_table("g_emolumento_periodo")

    # ----------------------------------------------------
    # Lista todos os registros de G_EMOLUMENTO_PERIODO
    # ----------------------------------------------------
    def index(self):
        # Importação da classe desejada
        index_service = self.dynamic_import.service("g_emolumento_periodo_index_service", "GEmolumentoPeriodoIndexService")

        # Instância da classe service
        self.index_service = index_service()

        # Execução da listagem
        return {
            "message": "Registros de G_EMOLUMENTO_PERIODO localizados com sucesso.",
            "data": self.index_service.execute(),
        }

    # ----------------------------------------------------
    # Busca um registro específico de G_EMOLUMENTO_PERIODO pelo ID
    # ----------------------------------------------------
    def show(self, g_emolumento_periodo_id_schema: GEmolumentoPeriodoIdSchema):
        # Importação da classe desejada
        show_service = self.dynamic_import.service("g_emolumento_periodo_show_service", "GEmolumentoPeriodoShowService")

        # Instância da classe service
        self.show_service = show_service()

        # Execução da busca
        return {
            "message": "Registro de G_EMOLUMENTO_PERIODO localizado com sucesso.",
            "data": self.show_service.execute(g_emolumento_periodo_id_schema),
        }

    # ----------------------------------------------------
    # Cadastra um novo registro em G_EMOLUMENTO_PERIODO
    # ----------------------------------------------------
    def save(self, g_emolumento_periodo_save_schema: GEmolumentoPeriodoSaveSchema):
        # Importação da classe desejada
        save_service = self.dynamic_import.service("g_emolumento_periodo_save_service", "GEmolumentoPeriodoSaveService")

        # Instância da classe service
        self.save_service = save_service()

        # Execução do salvamento
        return {
            "message": "Registro de G_EMOLUMENTO_PERIODO salvo com sucesso.",
            "data": self.save_service.execute(g_emolumento_periodo_save_schema),
        }

    # ----------------------------------------------------
    # Atualiza um registro existente de G_EMOLUMENTO_PERIODO
    # ----------------------------------------------------
    def update(self, g_emolumento_periodo_update_schema: GEmolumentoPeriodoUpdateSchema):
        # Importação da classe desejada
        update_service = self.dynamic_import.service("g_emolumento_periodo_update_service", "GEmolumentoPeriodoUpdateService")

        # Instância da classe service
        self.update_service = update_service()

        # Execução da atualização
        return {
            "message": "Registro de G_EMOLUMENTO_PERIODO atualizado com sucesso.",
            "data": self.update_service.execute(g_emolumento_periodo_update_schema),
        }

    # ----------------------------------------------------
    # Exclui um registro de G_EMOLUMENTO_PERIODO
    # ----------------------------------------------------
    def delete(self, g_emolumento_periodo_id_schema: GEmolumentoPeriodoIdSchema):
        # Importação da classe desejada
        delete_service = self.dynamic_import.service("g_emolumento_periodo_delete_service", "GEmolumentoPeriodoDeleteService")

        # Instância da classe service
        self.delete_service = delete_service()

        # Execução da exclusão
        return {
            "message": "Registro de G_EMOLUMENTO_PERIODO removido com sucesso.",
            "data": self.delete_service.execute(g_emolumento_periodo_id_schema),
        }
