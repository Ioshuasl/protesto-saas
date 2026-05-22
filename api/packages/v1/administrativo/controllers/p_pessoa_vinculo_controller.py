from actions.data.query_params_parser import QueryParams
from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.p_pessoa_vinculo_schema import (
    PPessoaVinculoIdSchema,
    PPessoaVinculoIndexSchema,
    PPessoaVinculoSaveSchema,
    PPessoaVinculoUpdateSchema,
)


class PPessoaVinculoController:
    def __init__(self):
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("administrativo")
        self.dynamic_import.set_table("p_pessoa_vinculo")

    def index(
        self,
        vinculo_index_schema: PPessoaVinculoIndexSchema,
        query_params: QueryParams,
    ):
        index_service = self.dynamic_import.service(
            "p_pessoa_vinculo_index_service",
            "IndexService",
        )
        result = index_service().execute(vinculo_index_schema, query_params)
        return {
            "message": "Vínculos de pessoa localizados com sucesso",
            "data": result["rows"],
            "pagination": result["pagination"],
        }

    def show(self, vinculo_schema: PPessoaVinculoIdSchema):
        show_service = self.dynamic_import.service(
            "p_pessoa_vinculo_show_service",
            "ShowService",
        )
        return {
            "message": "Vínculo de pessoa localizado com sucesso",
            "data": show_service().execute(vinculo_schema),
        }

    def save(self, vinculo_schema: PPessoaVinculoSaveSchema):
        save_service = self.dynamic_import.service(
            "p_pessoa_vinculo_save_service",
            "SaveService",
        )
        return {
            "message": "Vínculo de pessoa salvo com sucesso",
            "data": save_service().execute(vinculo_schema),
        }

    def update(self, pessoa_vinculo_id: int, vinculo_schema: PPessoaVinculoUpdateSchema):
        update_service = self.dynamic_import.service(
            "p_pessoa_vinculo_update_service",
            "UpdateService",
        )
        return {
            "message": "Vínculo de pessoa atualizado com sucesso",
            "data": update_service().execute(pessoa_vinculo_id, vinculo_schema),
        }

    def delete(self, vinculo_schema: PPessoaVinculoIdSchema):
        delete_service = self.dynamic_import.service(
            "p_pessoa_vinculo_delete_service",
            "DeleteService",
        )
        delete_service().execute(vinculo_schema)
        return {
            "message": "Vínculo de pessoa removido com sucesso",
            "data": True,
        }
