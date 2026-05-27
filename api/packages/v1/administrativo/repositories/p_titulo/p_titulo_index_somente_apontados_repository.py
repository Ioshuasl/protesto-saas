from __future__ import annotations

from typing import Any

from orm_py import Op

from packages.v1.administrativo.repositories.p_titulo.p_titulo_index_repository import (
    IndexRepository,
)
from packages.v1.administrativo.schemas.p_titulo_schema import PTituloIndexSchema

_SOMENTE_APONTADOS_DATE_CONDITIONS: list[dict[Any, Any]] = [
    {"DATA_CADASTRO": {Op.not_: None}},
    {"DATA_APONTAMENTO": {Op.not_: None}},
    {"DATA_INTIMACAO": {Op.is_: None}},
    {"DATA_PROTESTO": {Op.is_: None}},
    {"DATA_CANCELAMENTO": {Op.is_: None}},
    {"DATA_DESISTENCIA": {Op.is_: None}},
]


class IndexSomenteApontadosRepository(IndexRepository):
    @staticmethod
    def _build_base_orm_conditions(
        titulo_index_schema: PTituloIndexSchema,
    ) -> list[dict[Any, Any]]:
        conditions = IndexRepository._build_base_orm_conditions(titulo_index_schema)
        conditions.extend(_SOMENTE_APONTADOS_DATE_CONDITIONS)
        return conditions
