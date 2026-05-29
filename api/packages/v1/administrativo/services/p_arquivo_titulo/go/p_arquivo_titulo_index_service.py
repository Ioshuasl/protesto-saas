from actions.data.query_params_parser import QueryParams
from packages.v1.administrativo.actions.p_arquivo_titulo.p_arquivo_titulo_index_action import (
    IndexAction,
)
from packages.v1.administrativo.schemas.p_arquivo_titulo_schema import PArquivoTituloIndexSchema


class IndexService:
    def execute(
        self,
        arquivo_index_schema: PArquivoTituloIndexSchema,
        query_params: QueryParams,
    ):
        return IndexAction().execute(arquivo_index_schema, query_params)
