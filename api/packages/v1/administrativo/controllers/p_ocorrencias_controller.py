from actions.data.query_params_parser import QueryParams
from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.p_ocorrencias_schema import (
    POcorrenciasIdSchema,
    POcorrenciasIndexSchema,
    POcorrenciasSaveSchema,
    POcorrenciasUpdateSchema,
)


class POcorrenciasController:
    def __init__(self):
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("administrativo")
        self.dynamic_import.set_table("p_ocorrencias")

    def index(
        self, ocorrencias_index_schema: POcorrenciasIndexSchema, query_params: QueryParams
    ):
        index_service = self.dynamic_import.service(
            "p_ocorrencias_index_service",
            "IndexService",
        )
        result = index_service().execute(ocorrencias_index_schema, query_params)
        return {
            "message": "Ocorrências localizadas com sucesso",
            "data": result["rows"],
            "pagination": result["pagination"],
        }

    def show(self, ocorrencias_schema: POcorrenciasIdSchema):
        show_service = self.dynamic_import.service(
            "p_ocorrencias_show_service",
            "ShowService",
        )
        return {
            "message": "Ocorrência localizada com sucesso",
            "data": show_service().execute(ocorrencias_schema),
        }

    def save(self, ocorrencias_schema: POcorrenciasSaveSchema):
        save_service = self.dynamic_import.service(
            "p_ocorrencias_save_service",
            "SaveService",
        )
        return {
            "message": "Ocorrência salva com sucesso",
            "data": save_service().execute(ocorrencias_schema),
        }

    def update(self, ocorrencias_id: int, ocorrencias_schema: POcorrenciasUpdateSchema):
        update_service = self.dynamic_import.service(
            "p_ocorrencias_update_service",
            "UpdateService",
        )
        return {
            "message": "Ocorrência atualizada com sucesso",
            "data": update_service().execute(ocorrencias_id, ocorrencias_schema),
        }

    def delete(self, ocorrencias_schema: POcorrenciasIdSchema):
        delete_service = self.dynamic_import.service(
            "p_ocorrencias_delete_service",
            "DeleteService",
        )
        return {
            "message": "Ocorrência removida com sucesso",
            "data": delete_service().execute(ocorrencias_schema),
        }
