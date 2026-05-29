from packages.v1.administrativo.actions.p_arquivo_titulo.p_arquivo_titulo_show_action import (
    ShowAction,
)
from packages.v1.administrativo.schemas.p_arquivo_titulo_schema import PArquivoTituloShowSchema


class ShowService:
    def execute(self, arquivo_schema: PArquivoTituloShowSchema):
        return ShowAction().execute(arquivo_schema)
