from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_banco import get_p_banco_model
from packages.v1.administrativo.schemas.p_banco_schema import (
    PBancoIndexSchema,
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


class IndexRepository(BaseRepository):
    def execute(self, banco_index_schema: PBancoIndexSchema):
        if use_orm_firebird():
            return self._execute_orm(banco_index_schema)
        return self._execute_sql(banco_index_schema)

    def _execute_orm(self, banco_index_schema: PBancoIndexSchema) -> list[dict[str, Any]]:
        if self._has_string_filters(banco_index_schema):
            return self._execute_sql(banco_index_schema)

        rows = get_p_banco_model().findAll({"order": [("DESCRICAO", "ASC")]})
        return [self._map_banco_row(row) or {} for row in rows]

    def _execute_sql(self, banco_index_schema: PBancoIndexSchema) -> list[dict[str, Any]]:
        sql = f"""
        SELECT
            {_SELECT_COLUMNS.strip()}
        FROM P_BANCO
        """
        where: list[str] = []
        params = banco_index_schema.model_dump(exclude_none=True)

        if banco_index_schema.descricao is not None:
            where.append("UPPER(DESCRICAO) LIKE UPPER(:descricao)")
            params["descricao"] = f"%{banco_index_schema.descricao}%"
        if banco_index_schema.codigo is not None:
            where.append("UPPER(CODIGO_BANCO) LIKE UPPER(:codigo)")
            params["codigo"] = f"%{banco_index_schema.codigo}%"

        if where:
            sql += " WHERE " + " AND ".join(where)

        sql += " ORDER BY DESCRICAO ASC"
        rows = self.fetch_all(sql, params)
        return [self._map_banco_row(row) or {} for row in rows]

    @staticmethod
    def _has_string_filters(banco_index_schema: PBancoIndexSchema) -> bool:
        return any(
            [
                banco_index_schema.descricao is not None,
                banco_index_schema.codigo is not None,
            ]
        )

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
