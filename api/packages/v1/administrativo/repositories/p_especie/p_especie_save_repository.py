from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_especie import get_p_especie_model
from packages.v1.administrativo.schemas.p_especie_schema import (
    PEspecieSaveSchema,
    normalize_especie_from_db,
)

_SELECT_COLUMNS = """
    ESPECIE_ID,
    ESPECIE,
    DESCRICAO
"""


class SaveRepository(BaseRepository):
    def execute(self, especie_schema: PEspecieSaveSchema):
        if use_orm_firebird():
            return self._execute_orm(especie_schema)
        return self._execute_sql(especie_schema)

    def _execute_orm(self, especie_schema: PEspecieSaveSchema) -> dict[str, Any]:
        payload = {
            "ESPECIE_ID": especie_schema.especie_id,
            "ESPECIE": especie_schema.especie,
            "DESCRICAO": especie_schema.descricao,
        }
        created = get_p_especie_model().create(payload)
        return self._map_especie_row(created) or {}

    def _execute_sql(self, especie_schema: PEspecieSaveSchema) -> dict[str, Any]:
        try:
            sql = f"""
            INSERT INTO P_ESPECIE (
                ESPECIE_ID,
                ESPECIE,
                DESCRICAO
            ) VALUES (
                :especie_id,
                :especie,
                :descricao
            )
            RETURNING
                {_SELECT_COLUMNS.strip()};
            """
            params = {
                "especie_id": especie_schema.especie_id,
                "especie": especie_schema.especie,
                "descricao": especie_schema.descricao,
            }
            result = self.run_and_return(sql, params)
            return self._map_especie_row(result) or {}
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar espécie: {exc}",
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
