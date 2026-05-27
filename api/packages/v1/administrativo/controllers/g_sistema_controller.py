from typing import Union

from actions.data.query_params_parser import QueryParams
from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.g_sistema_schema import (
    GSistemaIdSchema,
    GSistemaIndexSchema,
    GSistemaSaveSchema,
    GSistemaUpdateSchema,
)


class GSistemaController:
    def __init__(self):
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("administrativo")
        self.dynamic_import.set_table("g_sistema")

    def index(
        self,
        sistema_index_schema: GSistemaIndexSchema,
        query_params: QueryParams,
    ):
        index_service = self.dynamic_import.service(
            "g_sistema_index_service",
            "IndexService",
        )
        result = index_service().execute(sistema_index_schema, query_params)
        return {
            "message": "Sistemas localizados com sucesso",
            "data": result["rows"],
            "pagination": result["pagination"],
        }

    def show(self, sistema_schema: GSistemaIdSchema):
        show_service = self.dynamic_import.service(
            "g_sistema_show_service",
            "ShowService",
        )
        return {
            "message": "Sistema localizado com sucesso",
            "data": show_service().execute(sistema_schema),
        }

    def save(self, sistema_schema: GSistemaSaveSchema):
        save_service = self.dynamic_import.service(
            "g_sistema_save_service",
            "SaveService",
        )
        return {
            "message": "Sistema salvo com sucesso",
            "data": save_service().execute(sistema_schema),
        }

    def update(
        self,
        sistema_id: Union[int, float],
        sistema_schema: GSistemaUpdateSchema,
    ):
        update_service = self.dynamic_import.service(
            "g_sistema_update_service",
            "UpdateService",
        )
        return {
            "message": "Sistema atualizado com sucesso",
            "data": update_service().execute(sistema_id, sistema_schema),
        }

    def delete(self, sistema_schema: GSistemaIdSchema):
        delete_service = self.dynamic_import.service(
            "g_sistema_delete_service",
            "DeleteService",
        )
        return {
            "message": "Sistema removido com sucesso",
            "data": delete_service().execute(sistema_schema),
        }
