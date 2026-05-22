from actions.data.query_params_parser import QueryParams
from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.p_titulo_schema import (
    PTituloIdSchema,
    PTituloIndexSchema,
    PTituloSaveSchema,
    PTituloUpdateSchema,
)


class PTituloController:
    def __init__(self):
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("administrativo")
        self.dynamic_import.set_table("p_titulo")

    def index(self, titulo_index_schema: PTituloIndexSchema, query_params: QueryParams):
        index_service = self.dynamic_import.service(
            "p_titulo_index_service",
            "IndexService",
        )
        result = index_service().execute(titulo_index_schema, query_params)
        return {
            "message": "Títulos localizados com sucesso",
            "data": result["rows"],
            "pagination": result["pagination"],
        }

    def show(self, titulo_schema: PTituloIdSchema):
        show_service = self.dynamic_import.service(
            "p_titulo_show_service",
            "ShowService",
        )
        return {
            "message": "Título localizado com sucesso",
            "data": show_service().execute(titulo_schema),
        }

    def selos(self, titulo_schema: PTituloIdSchema):
        selos_service = self.dynamic_import.service(
            "p_titulo_selos_service",
            "SelosService",
        )
        return {
            "message": "Selos do título localizados com sucesso",
            "data": selos_service().execute(titulo_schema),
        }

    def save(self, titulo_schema: PTituloSaveSchema):
        save_service = self.dynamic_import.service(
            "p_titulo_save_service",
            "SaveService",
        )
        return {
            "message": "Título salvo com sucesso",
            "data": save_service().execute(titulo_schema),
        }

    def update(self, titulo_id: int, titulo_schema: PTituloUpdateSchema):
        update_service = self.dynamic_import.service(
            "p_titulo_update_service",
            "UpdateService",
        )
        return {
            "message": "Título atualizado com sucesso",
            "data": update_service().execute(titulo_id, titulo_schema),
        }

    def delete(self, titulo_schema: PTituloIdSchema):
        delete_service = self.dynamic_import.service(
            "p_titulo_delete_service",
            "DeleteService",
        )
        return {
            "message": "Título removido com sucesso",
            "data": delete_service().execute(titulo_schema),
        }
