from actions.data.query_params_parser import QueryParams
from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.p_livro_natureza_schema import (
    PLivroNaturezaIdSchema,
    PLivroNaturezaIndexSchema,
    PLivroNaturezaSaveSchema,
    PLivroNaturezaUpdateSchema,
)


class PLivroNaturezaController:
    def __init__(self):
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("administrativo")
        self.dynamic_import.set_table("p_livro_natureza")

    def index(
        self,
        livro_natureza_index_schema: PLivroNaturezaIndexSchema,
        query_params: QueryParams,
    ):
        index_service = self.dynamic_import.service(
            "p_livro_natureza_index_service",
            "IndexService",
        )
        result = index_service().execute(livro_natureza_index_schema, query_params)
        return {
            "message": "Naturezas de livro localizadas com sucesso",
            "data": result["rows"],
            "pagination": result["pagination"],
        }

    def show(self, livro_natureza_schema: PLivroNaturezaIdSchema):
        show_service = self.dynamic_import.service(
            "p_livro_natureza_show_service",
            "ShowService",
        )
        return {
            "message": "Natureza de livro localizada com sucesso",
            "data": show_service().execute(livro_natureza_schema),
        }

    def save(self, livro_natureza_schema: PLivroNaturezaSaveSchema):
        save_service = self.dynamic_import.service(
            "p_livro_natureza_save_service",
            "SaveService",
        )
        return {
            "message": "Natureza de livro salva com sucesso",
            "data": save_service().execute(livro_natureza_schema),
        }

    def update(
        self, livro_natureza_id: int, livro_natureza_schema: PLivroNaturezaUpdateSchema
    ):
        update_service = self.dynamic_import.service(
            "p_livro_natureza_update_service",
            "UpdateService",
        )
        return {
            "message": "Natureza de livro atualizada com sucesso",
            "data": update_service().execute(livro_natureza_id, livro_natureza_schema),
        }

    def delete(self, livro_natureza_schema: PLivroNaturezaIdSchema):
        delete_service = self.dynamic_import.service(
            "p_livro_natureza_delete_service",
            "DeleteService",
        )
        return {
            "message": "Natureza de livro removida com sucesso",
            "data": delete_service().execute(livro_natureza_schema),
        }
