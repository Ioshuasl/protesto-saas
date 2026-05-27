from abstracts.action import BaseAction
from actions.data.query_params_parser import QueryParams
from packages.v1.administrativo.repositories.g_emolumento_item.g_emolumento_item_list_details_repository import (
    GEmolumentoItemListDetailsRepository,
)
from packages.v1.administrativo.schemas.g_emolumento_item_schema import (
    GEmolumentoItemListDetailsSchema,
)


class GEmolumentoItemListDetailsAction(BaseAction):
    def execute(self, data: GEmolumentoItemListDetailsSchema, query_params: QueryParams):
        repository = GEmolumentoItemListDetailsRepository()
        return repository.execute(data, query_params)
