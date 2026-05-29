from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_arquivo_titulo.p_arquivo_titulo_download_repository import (
    DownloadRepository,
)
from packages.v1.administrativo.schemas.p_arquivo_titulo_schema import PArquivoTituloIdSchema


class DownloadAction(BaseAction):
    def execute(self, arquivo_schema: PArquivoTituloIdSchema):
        return DownloadRepository().execute(arquivo_schema)
