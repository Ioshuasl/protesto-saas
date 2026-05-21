from actions.data.query_params_parser import QueryParams
from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.p_livro_andamento_schema import (
    PLivroAndamentoFinalizarSchema,
    PLivroAndamentoIdSchema,
    PLivroAndamentoIndexSchema,
    PLivroAndamentoNaturezaIdSchema,
    PLivroAndamentoSaveSchema,
    PLivroAndamentoUpdateSchema,
)


class PLivroAndamentoController:
    def __init__(self):
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("administrativo")
        self.dynamic_import.set_table("p_livro_andamento")

    def index(
        self,
        livro_andamento_index_schema: PLivroAndamentoIndexSchema,
        query_params: QueryParams,
    ):
        index_service = self.dynamic_import.service(
            "p_livro_andamento_index_service",
            "IndexService",
        )
        result = index_service().execute(livro_andamento_index_schema, query_params)
        return {
            "message": "Livros de andamento localizados com sucesso",
            "data": result["rows"],
            "pagination": result["pagination"],
        }

    def proximo_numero_livro(self, schema: PLivroAndamentoNaturezaIdSchema):
        service = self.dynamic_import.service(
            "p_livro_andamento_max_numero_livro_service",
            "MaxNumeroLivroService",
        )
        return {
            "message": "Sugestão de numeração localizada com sucesso",
            "data": service().execute(schema),
        }

    def show(self, livro_andamento_schema: PLivroAndamentoIdSchema):
        show_service = self.dynamic_import.service(
            "p_livro_andamento_show_service",
            "ShowService",
        )
        return {
            "message": "Livro de andamento localizado com sucesso",
            "data": show_service().execute(livro_andamento_schema),
        }

    def save(self, livro_andamento_schema: PLivroAndamentoSaveSchema):
        save_service = self.dynamic_import.service(
            "p_livro_andamento_save_service",
            "SaveService",
        )
        return {
            "message": "Livro de andamento salvo com sucesso",
            "data": save_service().execute(livro_andamento_schema),
        }

    def finalizar(
        self,
        livro_andamento_id: int,
        livro_andamento_schema: PLivroAndamentoFinalizarSchema,
    ):
        finalizar_service = self.dynamic_import.service(
            "p_livro_andamento_finalizar_service",
            "FinalizarService",
        )
        return {
            "message": "Livro de andamento finalizado com sucesso",
            "data": finalizar_service().execute(
                livro_andamento_id, livro_andamento_schema
            ),
        }

    def update(
        self, livro_andamento_id: int, livro_andamento_schema: PLivroAndamentoUpdateSchema
    ):
        update_service = self.dynamic_import.service(
            "p_livro_andamento_update_service",
            "UpdateService",
        )
        return {
            "message": "Livro de andamento atualizado com sucesso",
            "data": update_service().execute(livro_andamento_id, livro_andamento_schema),
        }

    def delete(self, livro_andamento_schema: PLivroAndamentoIdSchema):
        delete_service = self.dynamic_import.service(
            "p_livro_andamento_delete_service",
            "DeleteService",
        )
        return {
            "message": "Livro de andamento removido com sucesso",
            "data": delete_service().execute(livro_andamento_schema),
        }
