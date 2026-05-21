from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.g_cidade import get_g_cidade_model
from packages.v1.administrativo.schemas.g_cidade_schema import GCidadeUpdateSchema

_SELECT_COLUMNS = """
    CIDADE_ID,
    UF,
    CIDADE_NOME,
    CODIGO_IBGE,
    CODIGO_GYN
"""


class UpdateRepository(BaseRepository):
    def execute(self, cidade_id: int, g_cidade_schema: GCidadeUpdateSchema):
        if use_orm_firebird():
            return self._execute_orm(cidade_id, g_cidade_schema)
        return self._execute_sql(cidade_id, g_cidade_schema)

    def _execute_orm(
        self, cidade_id: int, g_cidade_schema: GCidadeUpdateSchema
    ) -> dict[str, Any]:
        values = {
            "UF": g_cidade_schema.uf,
            "CIDADE_NOME": g_cidade_schema.cidade_nome,
            "CODIGO_IBGE": g_cidade_schema.codigo_ibge,
            "CODIGO_GYN": g_cidade_schema.codigo_gyn,
        }
        model = get_g_cidade_model()
        result = model.update(values, {"where": {"CIDADE_ID": cidade_id}})
        rows = result.get("rows") if isinstance(result, dict) else None
        if rows:
            return self._map_row(rows[0]) or {}

        mapped = self._map_row(model.findByPk(cidade_id))
        if not mapped:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Nenhuma cidade localizada para esta solicitação",
            )
        return mapped

    def _execute_sql(
        self, cidade_id: int, g_cidade_schema: GCidadeUpdateSchema
    ) -> dict[str, Any]:
        try:
            sql = f"""
            UPDATE G_CIDADE SET
                UF = :uf,
                CIDADE_NOME = :cidade_nome,
                CODIGO_IBGE = :codigo_ibge,
                CODIGO_GYN = :codigo_gyn
            WHERE CIDADE_ID = :cidade_id
            RETURNING
                {_SELECT_COLUMNS.strip()};
            """
            params = {
                "cidade_id": cidade_id,
                "uf": g_cidade_schema.uf,
                "cidade_nome": g_cidade_schema.cidade_nome,
                "codigo_ibge": g_cidade_schema.codigo_ibge,
                "codigo_gyn": g_cidade_schema.codigo_gyn,
            }
            result = self.run_and_return(sql, params)
            return self._map_row(result) or {}
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar G_CIDADE: {exc}",
            ) from exc

    @staticmethod
    def _map_row(row: Optional[Mapping[str, Any]]) -> Optional[dict[str, Any]]:
        mapped = normalize_row_keys(row)
        if mapped is None:
            return None

        cidade_id = mapped.get("cidade_id")
        if isinstance(cidade_id, Decimal):
            mapped["cidade_id"] = int(cidade_id)

        uf = mapped.get("uf")
        if uf is not None:
            mapped["uf"] = str(uf).strip().upper() or None

        return mapped
