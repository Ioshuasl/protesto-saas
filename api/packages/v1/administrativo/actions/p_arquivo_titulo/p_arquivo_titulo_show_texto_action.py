from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_arquivo_titulo.p_arquivo_titulo_show_texto_repository import (
    ShowTextoRepository,
)
from packages.v1.administrativo.schemas.p_arquivo_titulo_schema import PArquivoTituloIdSchema


class ShowTextoAction(BaseAction):
    def execute(self, arquivo_schema: PArquivoTituloIdSchema):
        return ShowTextoRepository().execute(arquivo_schema)
