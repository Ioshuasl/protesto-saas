from actions.data.query_params_parser import QueryParams
from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.p_motivos_cancelamento_schema import (
    PMotivosCancelamentoIdSchema,
    PMotivosCancelamentoIndexSchema,
    PMotivosCancelamentoSaveSchema,
    PMotivosCancelamentoUpdateSchema,
)


class PMotivosCancelamentoController:
    def __init__(self):
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("administrativo")
        self.dynamic_import.set_table("p_motivos_cancelamento")

    def index(
        self,
        motivos_cancelamento_index_schema: PMotivosCancelamentoIndexSchema,
        query_params: QueryParams,
    ):
        index_service = self.dynamic_import.service(
            "p_motivos_cancelamento_index_service",
            "IndexService",
        )
        result = index_service().execute(motivos_cancelamento_index_schema, query_params)
        return {
            "message": "Motivos de cancelamento localizados com sucesso",
            "data": result["rows"],
            "pagination": result["pagination"],
        }

    def show(self, motivos_cancelamento_schema: PMotivosCancelamentoIdSchema):
        show_service = self.dynamic_import.service(
            "p_motivos_cancelamento_show_service",
            "ShowService",
        )
        return {
            "message": "Motivo de cancelamento localizado com sucesso",
            "data": show_service().execute(motivos_cancelamento_schema),
        }

    def save(self, motivos_cancelamento_schema: PMotivosCancelamentoSaveSchema):
        save_service = self.dynamic_import.service(
            "p_motivos_cancelamento_save_service",
            "SaveService",
        )
        return {
            "message": "Motivo de cancelamento salvo com sucesso",
            "data": save_service().execute(motivos_cancelamento_schema),
        }

    def update(
        self,
        motivos_cancelamento_id: int,
        motivos_cancelamento_schema: PMotivosCancelamentoUpdateSchema,
    ):
        update_service = self.dynamic_import.service(
            "p_motivos_cancelamento_update_service",
            "UpdateService",
        )
        return {
            "message": "Motivo de cancelamento atualizado com sucesso",
            "data": update_service().execute(
                motivos_cancelamento_id, motivos_cancelamento_schema
            ),
        }

    def delete(self, motivos_cancelamento_schema: PMotivosCancelamentoIdSchema):
        delete_service = self.dynamic_import.service(
            "p_motivos_cancelamento_delete_service",
            "DeleteService",
        )
        return {
            "message": "Motivo de cancelamento removido com sucesso",
            "data": delete_service().execute(motivos_cancelamento_schema),
        }
