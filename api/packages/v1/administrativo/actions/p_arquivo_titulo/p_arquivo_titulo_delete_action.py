from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_arquivo_titulo.p_arquivo_titulo_delete_repository import (
    DeleteRepository,
)
from packages.v1.administrativo.schemas.p_arquivo_titulo_schema import PArquivoTituloIdSchema


class DeleteAction(BaseAction):
    def execute(self, arquivo_schema: PArquivoTituloIdSchema) -> bool:
        return DeleteRepository().execute(arquivo_schema)
