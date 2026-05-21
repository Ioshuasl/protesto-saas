from abstracts.action import BaseAction
from actions.data.query_params_parser import QueryParams
from packages.v1.administrativo.repositories.p_livro_natureza.p_livro_natureza_index_repository import (
    IndexRepository,
)
from packages.v1.administrativo.schemas.p_livro_natureza_schema import PLivroNaturezaIndexSchema


class IndexAction(BaseAction):
    def execute(
        self,
        livro_natureza_index_schema: PLivroNaturezaIndexSchema,
        query_params: QueryParams,
    ):
        return IndexRepository().execute(livro_natureza_index_schema, query_params)
