from actions.data.query_params_parser import QueryParams
from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.p_especie_schema import (
    PEspecieIdSchema,
    PEspecieIndexSchema,
    PEspecieSaveSchema,
    PEspecieUpdateSchema,
)


class PEspecieController:
    def __init__(self):
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("administrativo")
        self.dynamic_import.set_table("p_especie")

    def index(self, especie_index_schema: PEspecieIndexSchema, query_params: QueryParams):
        index_service = self.dynamic_import.service(
            "p_especie_index_service",
            "IndexService",
        )
        result = index_service().execute(especie_index_schema, query_params)
        return {
            "message": "Espécies localizadas com sucesso",
            "data": result["rows"],
            "pagination": result["pagination"],
        }

    def show(self, especie_schema: PEspecieIdSchema):
        show_service = self.dynamic_import.service(
            "p_especie_show_service",
            "ShowService",
        )
        return {
            "message": "Espécie localizada com sucesso",
            "data": show_service().execute(especie_schema),
        }

    def save(self, especie_schema: PEspecieSaveSchema):
        save_service = self.dynamic_import.service(
            "p_especie_save_service",
            "SaveService",
        )
        return {
            "message": "Espécie salva com sucesso",
            "data": save_service().execute(especie_schema),
        }

    def update(self, especie_id: int, especie_schema: PEspecieUpdateSchema):
        update_service = self.dynamic_import.service(
            "p_especie_update_service",
            "UpdateService",
        )
        return {
            "message": "Espécie atualizada com sucesso",
            "data": update_service().execute(especie_id, especie_schema),
        }

    def delete(self, especie_schema: PEspecieIdSchema):
        delete_service = self.dynamic_import.service(
            "p_especie_delete_service",
            "DeleteService",
        )
        return {
            "message": "Espécie removida com sucesso",
            "data": delete_service().execute(especie_schema),
        }
