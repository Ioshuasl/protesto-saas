from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_banco import get_p_banco_model
from packages.v1.administrativo.schemas.p_banco_schema import (
    PBancoUpdateSchema,
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


class UpdateRepository(BaseRepository):
    def execute(self, banco_id: int, banco_schema: PBancoUpdateSchema):
        if use_orm_firebird():
            return self._execute_orm(banco_id, banco_schema)
        return self._execute_sql(banco_id, banco_schema)

    def _execute_orm(self, banco_id: int, banco_schema: PBancoUpdateSchema) -> dict[str, Any]:
        payload = banco_schema.model_dump(exclude_none=True)
        if not payload:
            row = get_p_banco_model().findByPk(banco_id)
            return self._map_banco_row(row) or {}

        orm_payload: dict[str, Any] = {}
        field_map = {
            "codigo_banco": "CODIGO_BANCO",
            "descricao": "DESCRICAO",
            "layout_id": "LAYOUT_ID",
            "apontamento_pag_posterior": "APONTAMENTO_PAG_POSTERIOR",
            "custas_na_confirmacao": "CUSTAS_NA_CONFIRMACAO",
        }
        for key, column in field_map.items():
            if key in payload:
                orm_payload[column] = payload[key]

        get_p_banco_model().update(orm_payload, {"where": {"BANCO_ID": banco_id}})
        row = get_p_banco_model().findByPk(banco_id)
        return self._map_banco_row(row) or {}

    def _execute_sql(self, banco_id: int, banco_schema: PBancoUpdateSchema) -> dict[str, Any]:
        payload = banco_schema.model_dump(exclude_none=True)
        if not payload:
            sql = f"""
            SELECT {_SELECT_COLUMNS.strip()}
            FROM P_BANCO
            WHERE BANCO_ID = :banco_id
            """
            row = self.fetch_one(sql, {"banco_id": banco_id})
            return self._map_banco_row(row) or {}

        set_parts: list[str] = []
        params: dict[str, Any] = {"banco_id": banco_id}
        field_map = {
            "codigo_banco": "CODIGO_BANCO",
            "descricao": "DESCRICAO",
            "layout_id": "LAYOUT_ID",
            "apontamento_pag_posterior": "APONTAMENTO_PAG_POSTERIOR",
            "custas_na_confirmacao": "CUSTAS_NA_CONFIRMACAO",
        }
        for key, column in field_map.items():
            if key in payload:
                set_parts.append(f"{column} = :{key}")
                params[key] = payload[key]

        try:
            sql = f"""
            UPDATE P_BANCO
            SET {", ".join(set_parts)}
            WHERE BANCO_ID = :banco_id
            RETURNING
                {_SELECT_COLUMNS.strip()};
            """
            result = self.run_and_return(sql, params)
            return self._map_banco_row(result) or {}
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar banco: {exc}",
            ) from exc

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
