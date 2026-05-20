from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.g_feriado_schema import (
    GFeriadoIdSchema,
    GFeriadoIndexSchema,
    GFeriadoSaveSchema,
    GFeriadoUpdateSchema,
)


class GFeriadoController:
    def __init__(self):
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("administrativo")
        self.dynamic_import.set_table("g_feriado")

    def index(self, feriado_index_schema: GFeriadoIndexSchema):
        index_service = self.dynamic_import.service(
            "g_feriado_index_service",
            "IndexService",
        )
        return {
            "message": "Feriados localizados com sucesso",
            "data": index_service().execute(feriado_index_schema),
        }

    def show(self, feriado_schema: GFeriadoIdSchema):
        show_service = self.dynamic_import.service(
            "g_feriado_show_service",
            "ShowService",
        )
        return {
            "message": "Feriado localizado com sucesso",
            "data": show_service().execute(feriado_schema),
        }

    def save(self, feriado_schema: GFeriadoSaveSchema):
        save_service = self.dynamic_import.service(
            "g_feriado_save_service",
            "SaveService",
        )
        return {
            "message": "Feriado salvo com sucesso",
            "data": save_service().execute(feriado_schema),
        }

    def update(self, feriado_id: int, feriado_schema: GFeriadoUpdateSchema):
        update_service = self.dynamic_import.service(
            "g_feriado_update_service",
            "UpdateService",
        )
        return {
            "message": "Feriado atualizado com sucesso",
            "data": update_service().execute(feriado_id, feriado_schema),
        }

    def delete(self, feriado_schema: GFeriadoIdSchema):
        delete_service = self.dynamic_import.service(
            "g_feriado_delete_service",
            "DeleteService",
        )
        return {
            "message": "Feriado removido com sucesso",
            "data": delete_service().execute(feriado_schema),
        }
