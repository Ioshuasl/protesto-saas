from abstracts.action import BaseAction
from actions.data.query_params_parser import QueryParams
from packages.v1.administrativo.repositories.p_livro_andamento.p_livro_andamento_index_repository import (
    IndexRepository,
)
from packages.v1.administrativo.schemas.p_livro_andamento_schema import PLivroAndamentoIndexSchema


class IndexAction(BaseAction):
    def execute(
        self,
        livro_andamento_index_schema: PLivroAndamentoIndexSchema,
        query_params: QueryParams,
    ):
        return IndexRepository().execute(livro_andamento_index_schema, query_params)
