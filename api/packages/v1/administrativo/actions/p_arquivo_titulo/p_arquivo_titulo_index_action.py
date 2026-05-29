from abstracts.action import BaseAction
from actions.data.query_params_parser import QueryParams
from packages.v1.administrativo.repositories.p_arquivo_titulo.p_arquivo_titulo_index_repository import (
    IndexRepository,
)
from packages.v1.administrativo.schemas.p_arquivo_titulo_schema import PArquivoTituloIndexSchema


class IndexAction(BaseAction):
    def execute(
        self,
        arquivo_index_schema: PArquivoTituloIndexSchema,
        query_params: QueryParams,
    ):
        return IndexRepository().execute(arquivo_index_schema, query_params)
