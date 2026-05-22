from actions.data.query_params_parser import QueryParams
from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.p_andamento_schema import (
    PAndamentoIdSchema,
    PAndamentoIndexByTituloSchema,
    PAndamentoIndexSchema,
    PAndamentoSaveSchema,
    PAndamentoUpdateSchema,
)


class PAndamentoController:
    def __init__(self):
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("administrativo")
        self.dynamic_import.set_table("p_andamento")

    def index_by_titulo(
        self,
        titulo_id: int,
        filter_schema: PAndamentoIndexByTituloSchema,
        query_params: QueryParams,
    ):
        index_service = self.dynamic_import.service(
            "p_andamento_index_by_titulo_service",
            "IndexByTituloService",
        )
        result = index_service().execute(titulo_id, filter_schema, query_params)
        return {
            "message": "Andamentos do título localizados com sucesso",
            "data": result["rows"],
            "pagination": result["pagination"],
        }

    def index(
        self, andamento_index_schema: PAndamentoIndexSchema, query_params: QueryParams
    ):
        index_service = self.dynamic_import.service(
            "p_andamento_index_service",
            "IndexService",
        )
        result = index_service().execute(andamento_index_schema, query_params)
        return {
            "message": "Andamentos localizados com sucesso",
            "data": result["rows"],
            "pagination": result["pagination"],
        }

    def show(self, andamento_schema: PAndamentoIdSchema):
        show_service = self.dynamic_import.service(
            "p_andamento_show_service",
            "ShowService",
        )
        return {
            "message": "Andamento localizado com sucesso",
            "data": show_service().execute(andamento_schema),
        }

    def save(self, andamento_schema: PAndamentoSaveSchema):
        save_service = self.dynamic_import.service(
            "p_andamento_save_service",
            "SaveService",
        )
        return {
            "message": "Andamento salvo com sucesso",
            "data": save_service().execute(andamento_schema),
        }

    def update(self, andamento_id: int, andamento_schema: PAndamentoUpdateSchema):
        update_service = self.dynamic_import.service(
            "p_andamento_update_service",
            "UpdateService",
        )
        return {
            "message": "Andamento atualizado com sucesso",
            "data": update_service().execute(andamento_id, andamento_schema),
        }

    def delete(self, andamento_schema: PAndamentoIdSchema):
        delete_service = self.dynamic_import.service(
            "p_andamento_delete_service",
            "DeleteService",
        )
        return {
            "message": "Andamento removido com sucesso",
            "data": delete_service().execute(andamento_schema),
        }
