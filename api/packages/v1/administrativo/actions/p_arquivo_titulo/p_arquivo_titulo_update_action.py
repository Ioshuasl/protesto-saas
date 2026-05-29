from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_arquivo_titulo.p_arquivo_titulo_update_repository import (
    UpdateRepository,
)
from packages.v1.administrativo.schemas.p_arquivo_titulo_schema import PArquivoTituloUpdateSchema


class UpdateAction(BaseAction):
    def execute(self, arquivo_titulo_id: int, arquivo_schema: PArquivoTituloUpdateSchema):
        return UpdateRepository().execute(arquivo_titulo_id, arquivo_schema)
