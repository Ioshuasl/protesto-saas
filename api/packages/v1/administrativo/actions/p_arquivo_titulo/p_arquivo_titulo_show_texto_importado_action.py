from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_arquivo_titulo.p_arquivo_titulo_show_texto_importado_repository import (
    ShowTextoImportadoRepository,
)
from packages.v1.administrativo.schemas.p_arquivo_titulo_schema import PArquivoTituloIdSchema


class ShowTextoImportadoAction(BaseAction):
    def execute(self, arquivo_schema: PArquivoTituloIdSchema):
        return ShowTextoImportadoRepository().execute(arquivo_schema)
