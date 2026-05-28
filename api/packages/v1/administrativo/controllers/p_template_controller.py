from actions.data.query_params_parser import QueryParams
from actions.dynamic_import.dynamic_import import DynamicImport
from fastapi import Request
from packages.v1.administrativo.schemas.p_template_schema import (
    PTemplateEditorCallbackSchema,
    PTemplateEditorOpenSchema,
    PTemplateIdSchema,
    PTemplateIndexSchema,
    PTemplateSaveSchema,
    PTemplateUpdateSchema,
)


class PTemplateController:
    def __init__(self):
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("administrativo")
        self.dynamic_import.set_table("p_template")

    def index(
        self,
        template_index_schema: PTemplateIndexSchema,
        query_params: QueryParams,
    ):
        index_service = self.dynamic_import.service(
            "p_template_index_service",
            "IndexService",
        )
        result = index_service().execute(template_index_schema, query_params)
        return {
            "message": "Templates localizados com sucesso",
            "data": result["rows"],
            "pagination": result["pagination"],
        }

    def show(self, template_schema: PTemplateIdSchema):
        show_service = self.dynamic_import.service(
            "p_template_show_service",
            "ShowService",
        )
        return {
            "message": "Template localizado com sucesso",
            "data": show_service().execute(template_schema),
        }

    def save(self, template_schema: PTemplateSaveSchema):
        save_service = self.dynamic_import.service(
            "p_template_save_service",
            "SaveService",
        )
        return {
            "message": "Template salvo com sucesso",
            "data": save_service().execute(template_schema),
        }

    def update(self, template_id: int, template_schema: PTemplateUpdateSchema):
        update_service = self.dynamic_import.service(
            "p_template_update_service",
            "UpdateService",
        )
        return {
            "message": "Template atualizado com sucesso",
            "data": update_service().execute(template_id, template_schema),
        }

    def delete(self, template_schema: PTemplateIdSchema):
        delete_service = self.dynamic_import.service(
            "p_template_delete_service",
            "DeleteService",
        )
        return {
            "message": "Template removido com sucesso",
            "data": delete_service().execute(template_schema),
        }

    def open_editor(
        self,
        template_id: int,
        request: Request,
        editor_schema: PTemplateEditorOpenSchema,
    ):
        open_editor_service = self.dynamic_import.service(
            "p_template_open_editor_service",
            "OpenEditorService",
        )
        return {
            "message": "Configuração do editor carregada com sucesso",
            "data": open_editor_service().execute(template_id, request, editor_schema),
        }

    def save_editor_callback(self, callback_schema: PTemplateEditorCallbackSchema):
        callback_service = self.dynamic_import.service(
            "p_template_save_editor_callback_service",
            "SaveEditorCallbackService",
        )
        return {
            "message": "Callback processado com sucesso",
            "data": callback_service().execute(callback_schema),
        }
