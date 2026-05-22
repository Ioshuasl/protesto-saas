from actions.data.query_params_parser import QueryParams
from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.p_pessoa_schema import (
    PPessoaIdSchema,
    PPessoaIndexSchema,
    PPessoaSaveSchema,
    PPessoaUpdateSchema,
)


class PPessoaController:
    def __init__(self):
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("administrativo")
        self.dynamic_import.set_table("p_pessoa")

    def index(
        self,
        pessoa_index_schema: PPessoaIndexSchema,
        query_params: QueryParams,
    ):
        index_service = self.dynamic_import.service(
            "p_pessoa_index_service",
            "IndexService",
        )
        result = index_service().execute(pessoa_index_schema, query_params)
        return {
            "message": "Pessoas localizadas com sucesso",
            "data": result["rows"],
            "pagination": result["pagination"],
        }

    def show(self, pessoa_schema: PPessoaIdSchema):
        show_service = self.dynamic_import.service(
            "p_pessoa_show_service",
            "ShowService",
        )
        return {
            "message": "Pessoa localizada com sucesso",
            "data": show_service().execute(pessoa_schema),
        }

    def save(self, pessoa_schema: PPessoaSaveSchema):
        save_service = self.dynamic_import.service(
            "p_pessoa_save_service",
            "SaveService",
        )
        return {
            "message": "Pessoa salva com sucesso",
            "data": save_service().execute(pessoa_schema),
        }

    def update(self, pessoa_id: int, pessoa_schema: PPessoaUpdateSchema):
        update_service = self.dynamic_import.service(
            "p_pessoa_update_service",
            "UpdateService",
        )
        return {
            "message": "Pessoa atualizada com sucesso",
            "data": update_service().execute(pessoa_id, pessoa_schema),
        }

    def delete(self, pessoa_schema: PPessoaIdSchema):
        delete_service = self.dynamic_import.service(
            "p_pessoa_delete_service",
            "DeleteService",
        )
        return {
            "message": "Pessoa removida com sucesso",
            "data": delete_service().execute(pessoa_schema),
        }
