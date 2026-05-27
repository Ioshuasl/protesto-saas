from actions.dynamic_import.dynamic_import import DynamicImport
from actions.data.query_params_parser import QueryParams
from packages.v1.administrativo.schemas.g_emolumento_item_schema import (
    GEmolumentoItemByTipoAtoSchema,
    GEmolumentoItemListDetailsSchema,
    GEmolumentoItemIndexSchema,
    GEmolumentoItemSaveSchema,
    GEmolumentoItemUpdateSchema,
    GEmolumentoItemIdSchema,
)


class GEmolumentoItemController:
    """
    Controller responsável por orquestrar as operações CRUD da tabela G_EMOLUMENTO_ITEM,
    utilizando carregamento dinâmico de serviços via DynamicImport.
    """

    def __init__(self):
        # ----------------------------------------------------
        # Inicialização do DynamicImport
        # ----------------------------------------------------
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("administrativo")
        self.dynamic_import.set_table("g_emolumento_item")

    # ----------------------------------------------------
    # Lista todos os registros de G_EMOLUMENTO_ITEM
    # ----------------------------------------------------
    def index(
        self, g_emolumento_item_emolumento_index_schema: GEmolumentoItemIndexSchema
    ):

        # Importação da classe desejada
        index_service = self.dynamic_import.service(
            "g_emolumento_item_index_service", "GEmolumentoItemIndexService"
        )

        # Instância da classe service
        self.index_service = index_service()

        # Execução da listagem
        return {
            "message": "Registros de G_EMOLUMENTO_ITEM localizados com sucesso.",
            "data": self.index_service.execute(
                g_emolumento_item_emolumento_index_schema
            ),
        }

    # ----------------------------------------------------
    # Lista todos os registros de G_EMOLUMENTO_ITEM
    # ----------------------------------------------------
    def get_by_tipo_ato(self, data: GEmolumentoItemByTipoAtoSchema):

        # Importação da classe desejada
        service = self.dynamic_import.service(
            "g_emolumento_item_by_tipo_ato_service", "GEmolumentoItemByTipoAtoService"
        )

        # Instância da classe service
        self.service = service()

        # Execução da listagem
        return {
            "message": "Registros de G_EMOLUMENTO_ITEM localizados com sucesso.",
            "data": self.service.execute(data),
        }

    # ----------------------------------------------------
    # Lista detalhada de G_EMOLUMENTO_ITEM com includes
    # ----------------------------------------------------
    def list_details(
        self, data: GEmolumentoItemListDetailsSchema, query_params: QueryParams
    ):
        service = self.dynamic_import.service(
            "g_emolumento_item_list_details_service",
            "GEmolumentoItemListDetailsService",
        )

        self.service = service()
        result = self.service.execute(data, query_params)

        return {
            "message": "Registros detalhados de G_EMOLUMENTO_ITEM localizados com sucesso.",
            "data": result["rows"],
            "pagination": result["pagination"],
        }

    # ----------------------------------------------------
    # Busca um registro específico de G_EMOLUMENTO_ITEM pelo ID
    # ----------------------------------------------------
    def show(self, g_emolumento_item_id_schema: GEmolumentoItemIdSchema):
        # Importação da classe desejada
        show_service = self.dynamic_import.service(
            "g_emolumento_item_show_service", "GEmolumentoItemShowService"
        )

        # Instância da classe service
        self.show_service = show_service()

        # Execução da busca
        return {
            "message": "Registro de G_EMOLUMENTO_ITEM localizado com sucesso.",
            "data": self.show_service.execute(g_emolumento_item_id_schema),
        }

    # ----------------------------------------------------
    # Cadastra um novo registro em G_EMOLUMENTO_ITEM
    # ----------------------------------------------------
    def save(self, g_emolumento_item_save_schema: GEmolumentoItemSaveSchema):
        # Importação da classe desejada
        save_service = self.dynamic_import.service(
            "g_emolumento_item_save_service", "GEmolumentoItemSaveService"
        )

        # Instância da classe service
        self.save_service = save_service()

        # Execução do salvamento
        return {
            "message": "Registro de G_EMOLUMENTO_ITEM salvo com sucesso.",
            "data": self.save_service.execute(g_emolumento_item_save_schema),
        }

    # ----------------------------------------------------
    # Atualiza um registro existente de G_EMOLUMENTO_ITEM
    # ----------------------------------------------------
    def update(self, g_emolumento_item_update_schema: GEmolumentoItemUpdateSchema):
        # Importação da classe desejada
        update_service = self.dynamic_import.service(
            "g_emolumento_item_update_service", "GEmolumentoItemUpdateService"
        )

        # Instância da classe service
        self.update_service = update_service()

        # Execução da atualização
        return {
            "message": "Registro de G_EMOLUMENTO_ITEM atualizado com sucesso.",
            "data": self.update_service.execute(g_emolumento_item_update_schema),
        }

    # ----------------------------------------------------
    # Exclui um registro de G_EMOLUMENTO_ITEM
    # ----------------------------------------------------
    def delete(self, g_emolumento_item_id_schema: GEmolumentoItemIdSchema):
        # Importação da classe desejada
        delete_service = self.dynamic_import.service(
            "g_emolumento_item_delete_service", "GEmolumentoItemDeleteService"
        )

        # Instância da classe service
        self.delete_service = delete_service()

        # Execução da exclusão
        return {
            "message": "Registro de G_EMOLUMENTO_ITEM removido com sucesso.",
            "data": self.delete_service.execute(g_emolumento_item_id_schema),
        }
