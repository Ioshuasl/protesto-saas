from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.g_selo_livro_schema import (
    GSeloLivroIdSchema,
    GSeloLivroSaveSchema,
    GSeloLivroUpdateSchema,
)


class GSeloLivroController:
    def __init__(self):
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("administrativo")
        self.dynamic_import.set_table("g_selo_livro")

    def index(self):
        service = self.dynamic_import.service(
            "g_selo_livro_index_service", "GSeloLivroIndexService"
        )

        return {
            "message": "Registros de G_SELO_LIVRO localizados com sucesso.",
            "data": service().execute(),
        }

    def show(self, data: GSeloLivroIdSchema):
        service = self.dynamic_import.service(
            "g_selo_livro_show_service", "GSeloLivroShowService"
        )

        return {
            "message": "Registro de G_SELO_LIVRO localizado com sucesso.",
            "data": service().execute(data),
        }

    def save(self, data: GSeloLivroSaveSchema):
        service = self.dynamic_import.service(
            "g_selo_livro_save_service", "GSeloLivroSaveService"
        )

        return {
            "message": "Registro de G_SELO_LIVRO salvo com sucesso.",
            "data": service().execute(data),
        }

    def update(self, data: GSeloLivroUpdateSchema):
        service = self.dynamic_import.service(
            "g_selo_livro_update_service", "GSeloLivroUpdateService"
        )

        return {
            "message": "Registro de G_SELO_LIVRO atualizado com sucesso.",
            "data": service().execute(data),
        }

    def delete(self, data: GSeloLivroIdSchema):
        service = self.dynamic_import.service(
            "g_selo_livro_delete_service", "GSeloLivroDeleteService"
        )

        return {
            "message": "Registro de G_SELO_LIVRO removido com sucesso.",
            "data": service().execute(data),
        }
