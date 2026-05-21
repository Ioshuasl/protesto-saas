from actions.data.query_params_parser import QueryParams
from packages.v1.administrativo.actions.p_livro_natureza.p_livro_natureza_index_action import (
    IndexAction,
)
from packages.v1.administrativo.schemas.p_livro_natureza_schema import PLivroNaturezaIndexSchema


class IndexService:
    def execute(
        self,
        livro_natureza_index_schema: PLivroNaturezaIndexSchema,
        query_params: QueryParams,
    ):
        return IndexAction().execute(livro_natureza_index_schema, query_params)
