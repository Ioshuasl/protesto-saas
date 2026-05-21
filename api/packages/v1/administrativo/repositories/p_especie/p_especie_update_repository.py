from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_especie import get_p_especie_model
from packages.v1.administrativo.schemas.p_especie_schema import (
    PEspecieUpdateSchema,
    normalize_especie_from_db,
)

_SELECT_COLUMNS = """
    ESPECIE_ID,
    ESPECIE,
    DESCRICAO
"""


class UpdateRepository(BaseRepository):
    def execute(self, especie_id: int, especie_schema: PEspecieUpdateSchema):
        if use_orm_firebird():
            return self._execute_orm(especie_id, especie_schema)
        return self._execute_sql(especie_id, especie_schema)

    def _execute_orm(self, especie_id: int, especie_schema: PEspecieUpdateSchema) -> dict[str, Any]:
        payload = especie_schema.model_dump(exclude_none=True)
        if not payload:
            row = get_p_especie_model().findByPk(especie_id)
            return self._map_especie_row(row) or {}

        orm_payload: dict[str, Any] = {}
        field_map = {
            "especie": "ESPECIE",
            "descricao": "DESCRICAO",
        }
        for key, column in field_map.items():
            if key in payload:
                orm_payload[column] = payload[key]

        get_p_especie_model().update(orm_payload, {"where": {"ESPECIE_ID": especie_id}})
        row = get_p_especie_model().findByPk(especie_id)
        return self._map_especie_row(row) or {}

    def _execute_sql(self, especie_id: int, especie_schema: PEspecieUpdateSchema) -> dict[str, Any]:
        payload = especie_schema.model_dump(exclude_none=True)
        if not payload:
            sql = f"""
            SELECT {_SELECT_COLUMNS.strip()}
            FROM P_ESPECIE
            WHERE ESPECIE_ID = :especie_id
            """
            row = self.fetch_one(sql, {"especie_id": especie_id})
            return self._map_especie_row(row) or {}

        set_parts: list[str] = []
        params: dict[str, Any] = {"especie_id": especie_id}
        field_map = {
            "especie": "ESPECIE",
            "descricao": "DESCRICAO",
        }
        for key, column in field_map.items():
            if key in payload:
                set_parts.append(f"{column} = :{key}")
                params[key] = payload[key]

        try:
            sql = f"""
            UPDATE P_ESPECIE
            SET {", ".join(set_parts)}
            WHERE ESPECIE_ID = :especie_id
            RETURNING
                {_SELECT_COLUMNS.strip()};
            """
            result = self.run_and_return(sql, params)
            return self._map_especie_row(result) or {}
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar espécie: {exc}",
            ) from exc

    @staticmethod
    def _map_especie_row(row: Optional[Mapping[str, Any]]) -> Optional[dict[str, Any]]:
        mapped = normalize_row_keys(row)
        if mapped is None:
            return None

        especie_id = mapped.get("especie_id")
        if isinstance(especie_id, Decimal):
            mapped["especie_id"] = int(especie_id)

        mapped["especie"] = normalize_especie_from_db(mapped.get("especie"))

        descricao = mapped.get("descricao")
        if descricao is not None:
            mapped["descricao"] = str(descricao).strip() or None

        return mapped
