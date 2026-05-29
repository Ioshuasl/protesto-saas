from packages.v1.administrativo.actions.p_arquivo_titulo.p_arquivo_titulo_show_texto_importado_action import (
    ShowTextoImportadoAction,
)
from packages.v1.administrativo.schemas.p_arquivo_titulo_schema import PArquivoTituloIdSchema


class ShowTextoImportadoService:
    def execute(self, arquivo_schema: PArquivoTituloIdSchema):
        return ShowTextoImportadoAction().execute(arquivo_schema)
