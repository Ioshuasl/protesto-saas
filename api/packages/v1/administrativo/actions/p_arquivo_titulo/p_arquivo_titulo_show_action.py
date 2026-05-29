from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_arquivo_titulo.p_arquivo_titulo_show_repository import (
    ShowRepository,
)
from packages.v1.administrativo.schemas.p_arquivo_titulo_schema import PArquivoTituloShowSchema


class ShowAction(BaseAction):
    def execute(self, arquivo_schema: PArquivoTituloShowSchema):
        return ShowRepository().execute(arquivo_schema)
