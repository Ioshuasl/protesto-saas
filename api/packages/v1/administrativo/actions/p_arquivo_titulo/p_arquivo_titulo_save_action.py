from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_arquivo_titulo.p_arquivo_titulo_save_repository import (
    SaveRepository,
)
from packages.v1.administrativo.schemas.p_arquivo_titulo_schema import PArquivoTituloSaveSchema


class SaveAction(BaseAction):
    def execute(self, arquivo_schema: PArquivoTituloSaveSchema):
        return SaveRepository().execute(arquivo_schema)
