from actions.data.query_params_parser import QueryParams
from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.p_motivos_schema import (
    PMotivosIdSchema,
    PMotivosIndexSchema,
    PMotivosSaveSchema,
    PMotivosUpdateSchema,
)


class PMotivosController:
    def __init__(self):
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("administrativo")
        self.dynamic_import.set_table("p_motivos")

    def index(self, motivos_index_schema: PMotivosIndexSchema, query_params: QueryParams):
        index_service = self.dynamic_import.service(
            "p_motivos_index_service",
            "IndexService",
        )
        result = index_service().execute(motivos_index_schema, query_params)
        return {
            "message": "Motivos localizados com sucesso",
            "data": result["rows"],
            "pagination": result["pagination"],
        }

    def show(self, motivos_schema: PMotivosIdSchema):
        show_service = self.dynamic_import.service(
            "p_motivos_show_service",
            "ShowService",
        )
        return {
            "message": "Motivo localizado com sucesso",
            "data": show_service().execute(motivos_schema),
        }

    def save(self, motivos_schema: PMotivosSaveSchema):
        save_service = self.dynamic_import.service(
            "p_motivos_save_service",
            "SaveService",
        )
        return {
            "message": "Motivo salvo com sucesso",
            "data": save_service().execute(motivos_schema),
        }

    def update(self, motivos_id: int, motivos_schema: PMotivosUpdateSchema):
        update_service = self.dynamic_import.service(
            "p_motivos_update_service",
            "UpdateService",
        )
        return {
            "message": "Motivo atualizado com sucesso",
            "data": update_service().execute(motivos_id, motivos_schema),
        }

    def delete(self, motivos_schema: PMotivosIdSchema):
        delete_service = self.dynamic_import.service(
            "p_motivos_delete_service",
            "DeleteService",
        )
        return {
            "message": "Motivo removido com sucesso",
            "data": delete_service().execute(motivos_schema),
        }
