from actions.data.query_params_parser import QueryParams
from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.p_arquivo_titulo_schema import (
    PArquivoTituloIdSchema,
    PArquivoTituloIndexSchema,
    PArquivoTituloSaveSchema,
    PArquivoTituloShowSchema,
    PArquivoTituloUpdateSchema,
)


class PArquivoTituloController:
    def __init__(self):
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("administrativo")
        self.dynamic_import.set_table("p_arquivo_titulo")

    def index(
        self,
        arquivo_index_schema: PArquivoTituloIndexSchema,
        query_params: QueryParams,
    ):
        index_service = self.dynamic_import.service(
            "p_arquivo_titulo_index_service",
            "IndexService",
        )
        result = index_service().execute(arquivo_index_schema, query_params)
        return {
            "message": "Arquivos de título localizados com sucesso",
            "data": result["rows"],
            "pagination": result["pagination"],
        }

    def show(self, arquivo_schema: PArquivoTituloShowSchema):
        show_service = self.dynamic_import.service(
            "p_arquivo_titulo_show_service",
            "ShowService",
        )
        return {
            "message": "Arquivo de título localizado com sucesso",
            "data": show_service().execute(arquivo_schema),
        }

    def save(self, arquivo_schema: PArquivoTituloSaveSchema):
        save_service = self.dynamic_import.service(
            "p_arquivo_titulo_save_service",
            "SaveService",
        )
        return {
            "message": "Arquivo de título salvo com sucesso",
            "data": save_service().execute(arquivo_schema),
        }

    def update(self, arquivo_titulo_id: int, arquivo_schema: PArquivoTituloUpdateSchema):
        update_service = self.dynamic_import.service(
            "p_arquivo_titulo_update_service",
            "UpdateService",
        )
        return {
            "message": "Arquivo de título atualizado com sucesso",
            "data": update_service().execute(arquivo_titulo_id, arquivo_schema),
        }

    def delete(self, arquivo_schema: PArquivoTituloIdSchema):
        delete_service = self.dynamic_import.service(
            "p_arquivo_titulo_delete_service",
            "DeleteService",
        )
        delete_service().execute(arquivo_schema)
        return {
            "message": "Arquivo de título removido com sucesso",
            "data": True,
        }

    def show_texto(self, arquivo_schema: PArquivoTituloIdSchema):
        show_texto_service = self.dynamic_import.service(
            "p_arquivo_titulo_show_texto_service",
            "ShowTextoService",
        )
        return {
            "message": "Texto do arquivo localizado com sucesso",
            "data": show_texto_service().execute(arquivo_schema),
        }

    def show_texto_importado(self, arquivo_schema: PArquivoTituloIdSchema):
        show_texto_importado_service = self.dynamic_import.service(
            "p_arquivo_titulo_show_texto_importado_service",
            "ShowTextoImportadoService",
        )
        return {
            "message": "Texto importado do arquivo localizado com sucesso",
            "data": show_texto_importado_service().execute(arquivo_schema),
        }

    def download(self, arquivo_schema: PArquivoTituloIdSchema):
        download_service = self.dynamic_import.service(
            "p_arquivo_titulo_download_service",
            "DownloadService",
        )
        return download_service().execute(arquivo_schema)
