from packages.v1.administrativo.schemas.t_livro_natureza_schema import (
    TLivroNaturezaIdSchema,
    TLivroNaturezaSaveSchema,
    TLivroNaturezaShowModeloSchema,
    TLivroNaturezaUpdateSchema,
)
from packages.v1.administrativo.services.t_livro_natureza.go.t_livro_natureza_delete_service import TLivroNaturezaDeleteService
from packages.v1.administrativo.services.t_livro_natureza.go.t_livro_natureza_index_service import TLivroNaturezaIndexService
from packages.v1.administrativo.services.t_livro_natureza.go.t_livro_natureza_save_service import TLivroNaturezaSaveService
from packages.v1.administrativo.services.t_livro_natureza.go.t_livro_natureza_show_modelo_service import TLivroNaturezaShowModeloService
from packages.v1.administrativo.services.t_livro_natureza.go.t_livro_natureza_show_service import TLivroNaturezaShowService
from packages.v1.administrativo.services.t_livro_natureza.go.t_livro_natureza_update_modelo_texto_service import TLivroNaturezaUpdateModeloTextoService
from packages.v1.administrativo.services.t_livro_natureza.go.t_livro_natureza_update_service import TLivroNaturezaUpdateService


class TLivroNaturezaController:
    """Controller para orquestrar o CRUD de T_LIVRO_NATUREZA."""

    def index(self):
        return {
            "message": "Registros de T_LIVRO_NATUREZA localizados com sucesso.",
            "data": TLivroNaturezaIndexService().execute(),
        }

    def show(self, schema: TLivroNaturezaShowModeloSchema):
        return {
            "message": "Registro de T_LIVRO_NATUREZA localizado com sucesso.",
            "data": TLivroNaturezaShowService().execute(schema),
        }

    def show_modelo(self, schema: TLivroNaturezaShowModeloSchema):
        return {
            "message": "Registro de T_LIVRO_NATUREZA localizado com sucesso.",
            "data": TLivroNaturezaShowModeloService().execute(schema),
        }

    def save(self, schema: TLivroNaturezaSaveSchema):
        return {
            "message": "Registro de T_LIVRO_NATUREZA salvo com sucesso.",
            "data": TLivroNaturezaSaveService().execute(schema),
        }

    def update(self, schema: TLivroNaturezaUpdateSchema):
        return {
            "message": "Registro de T_LIVRO_NATUREZA atualizado com sucesso.",
            "data": TLivroNaturezaUpdateService().execute(schema),
        }

    def update_modelo_texto(self, schema: TLivroNaturezaUpdateSchema):
        return {
            "message": "Registro de T_LIVRO_NATUREZA atualizado com sucesso.",
            "data": TLivroNaturezaUpdateModeloTextoService().execute(schema),
        }

    def delete(self, schema: TLivroNaturezaIdSchema):
        return {
            "message": "Registro de T_LIVRO_NATUREZA removido com sucesso.",
            "data": TLivroNaturezaDeleteService().execute(schema),
        }
