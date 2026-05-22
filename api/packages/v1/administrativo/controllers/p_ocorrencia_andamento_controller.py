from actions.data.query_params_parser import QueryParams
from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.p_ocorrencia_andamento_schema import (
    POcorrenciaAndamentoIdSchema,
    POcorrenciaAndamentoIndexSchema,
    POcorrenciaAndamentoSaveSchema,
    POcorrenciaAndamentoUpdateSchema,
)


class POcorrenciaAndamentoController:
    def __init__(self):
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("administrativo")
        self.dynamic_import.set_table("p_ocorrencia_andamento")

    def index(
        self,
        ocorrencia_andamento_index_schema: POcorrenciaAndamentoIndexSchema,
        query_params: QueryParams,
    ):
        index_service = self.dynamic_import.service(
            "p_ocorrencia_andamento_index_service",
            "IndexService",
        )
        result = index_service().execute(ocorrencia_andamento_index_schema, query_params)
        return {
            "message": "Ocorrências de andamento localizadas com sucesso",
            "data": result["rows"],
            "pagination": result["pagination"],
        }

    def show(self, ocorrencia_andamento_schema: POcorrenciaAndamentoIdSchema):
        show_service = self.dynamic_import.service(
            "p_ocorrencia_andamento_show_service",
            "ShowService",
        )
        return {
            "message": "Ocorrência de andamento localizada com sucesso",
            "data": show_service().execute(ocorrencia_andamento_schema),
        }

    def save(self, ocorrencia_andamento_schema: POcorrenciaAndamentoSaveSchema):
        save_service = self.dynamic_import.service(
            "p_ocorrencia_andamento_save_service",
            "SaveService",
        )
        return {
            "message": "Ocorrência de andamento salva com sucesso",
            "data": save_service().execute(ocorrencia_andamento_schema),
        }

    def update(
        self,
        ocorrencia_andamento_id: int,
        ocorrencia_andamento_schema: POcorrenciaAndamentoUpdateSchema,
    ):
        update_service = self.dynamic_import.service(
            "p_ocorrencia_andamento_update_service",
            "UpdateService",
        )
        return {
            "message": "Ocorrência de andamento atualizada com sucesso",
            "data": update_service().execute(
                ocorrencia_andamento_id, ocorrencia_andamento_schema
            ),
        }

    def delete(self, ocorrencia_andamento_schema: POcorrenciaAndamentoIdSchema):
        delete_service = self.dynamic_import.service(
            "p_ocorrencia_andamento_delete_service",
            "DeleteService",
        )
        return {
            "message": "Ocorrência de andamento removida com sucesso",
            "data": delete_service().execute(ocorrencia_andamento_schema),
        }
