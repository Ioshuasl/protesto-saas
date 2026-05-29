from packages.v1.administrativo.actions.p_arquivo_titulo.p_arquivo_titulo_show_texto_action import (
    ShowTextoAction,
)
from packages.v1.administrativo.schemas.p_arquivo_titulo_schema import PArquivoTituloIdSchema


class ShowTextoService:
    def execute(self, arquivo_schema: PArquivoTituloIdSchema):
        return ShowTextoAction().execute(arquivo_schema)
