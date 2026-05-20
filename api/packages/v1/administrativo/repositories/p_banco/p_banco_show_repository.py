from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_banco import get_p_banco_model
from packages.v1.administrativo.schemas.p_banco_schema import (
    PBancoIdSchema,
    normalize_sim_nao_from_db,
)

_SELECT_COLUMNS = """
    BANCO_ID,
    CODIGO_BANCO,
    DESCRICAO,
    PESSOA_ID,
    LAYOUT_ID,
    APONTAMENTO_PAG_POSTERIOR,
    CUSTAS_NA_CONFIRMACAO,
    DEMAIS_DESPESAS
"""


class ShowRepository(BaseRepository):
    def execute(self, banco_schema: PBancoIdSchema):
        if use_orm_firebird():
            return self._execute_orm(banco_schema)
        return self._execute_sql(banco_schema)

    def _execute_orm(self, banco_schema: PBancoIdSchema) -> Optional[dict[str, Any]]:
        row = get_p_banco_model().findByPk(banco_schema.banco_id)
        return self._map_banco_row(row)

    def _execute_sql(self, banco_schema: PBancoIdSchema) -> Optional[dict[str, Any]]:
        sql = f"""
        SELECT
            {_SELECT_COLUMNS.strip()}
        FROM P_BANCO
        WHERE BANCO_ID = :banco_id
        """
        row = self.fetch_one(sql, {"banco_id": banco_schema.banco_id})
        return self._map_banco_row(row)

    @staticmethod
    def _map_banco_row(row: Optional[Mapping[str, Any]]) -> Optional[dict[str, Any]]:
        mapped = normalize_row_keys(row)
        if mapped is None:
            return None

        for key in ("banco_id", "pessoa_id", "layout_id"):
            value = mapped.get(key)
            if isinstance(value, Decimal):
                mapped[key] = int(value)

        demais = mapped.get("demais_despesas")
        if isinstance(demais, Decimal):
            mapped["demais_despesas"] = float(demais) if demais is not None else None
        if demais is None:
            mapped["demais_despesas"] = None

        mapped["apontamento_pag_posterior"] = normalize_sim_nao_from_db(
            mapped.get("apontamento_pag_posterior")
        )
        mapped["custas_na_confirmacao"] = normalize_sim_nao_from_db(
            mapped.get("custas_na_confirmacao")
        )

        codigo = mapped.get("codigo_banco")
        if codigo is not None:
            mapped["codigo_banco"] = str(codigo).strip() or None

        return mapped
