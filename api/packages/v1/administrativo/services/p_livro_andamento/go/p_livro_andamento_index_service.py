from actions.data.query_params_parser import QueryParams
from packages.v1.administrativo.actions.p_livro_andamento.p_livro_andamento_index_action import (
    IndexAction,
)
from packages.v1.administrativo.schemas.p_livro_andamento_schema import PLivroAndamentoIndexSchema


class IndexService:
    def execute(
        self,
        livro_andamento_index_schema: PLivroAndamentoIndexSchema,
        query_params: QueryParams,
    ):
        return IndexAction().execute(livro_andamento_index_schema, query_params)
