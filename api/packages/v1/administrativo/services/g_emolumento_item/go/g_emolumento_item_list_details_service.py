from fastapi import HTTPException, status
from actions.data.query_params_parser import QueryParams
from packages.v1.administrativo.actions.g_emolumento_item.g_emolumento_item_list_details_action import (
    GEmolumentoItemListDetailsAction,
)
from packages.v1.administrativo.schemas.g_emolumento_item_schema import (
    GEmolumentoItemListDetailsSchema,
)


class GEmolumentoItemListDetailsService:
    def execute(self, data: GEmolumentoItemListDetailsSchema, query_params: QueryParams):
        action = GEmolumentoItemListDetailsAction()
        response = action.execute(data, query_params)

        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar registros de G_EMOLUMENTO_ITEM.",
            )

        return response
