from fastapi import HTTPException, status

from actions.data.query_params_parser import QueryParams
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.actions.p_andamento.p_andamento_index_by_titulo_action import (
    IndexByTituloAction,
)
from packages.v1.administrativo.model.p_titulo import get_p_titulo_model
from packages.v1.administrativo.schemas.p_andamento_schema import PAndamentoIndexByTituloSchema


class IndexByTituloService:
    def _ensure_titulo_exists(self, titulo_id: int) -> None:
        if not use_orm_firebird():
            return
        row = get_p_titulo_model().findByPk(titulo_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Título não encontrado.",
            )

    def execute(
        self,
        titulo_id: int,
        filter_schema: PAndamentoIndexByTituloSchema,
        query_params: QueryParams,
    ):
        self._ensure_titulo_exists(titulo_id)
        return IndexByTituloAction().execute(titulo_id, filter_schema, query_params)
