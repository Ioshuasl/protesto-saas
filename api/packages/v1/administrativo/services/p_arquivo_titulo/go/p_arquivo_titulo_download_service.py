from packages.v1.administrativo.actions.p_arquivo_titulo.p_arquivo_titulo_download_action import (
    DownloadAction,
)
from packages.v1.administrativo.schemas.p_arquivo_titulo_schema import PArquivoTituloIdSchema


class DownloadService:
    def execute(self, arquivo_schema: PArquivoTituloIdSchema):
        return DownloadAction().execute(arquivo_schema)
