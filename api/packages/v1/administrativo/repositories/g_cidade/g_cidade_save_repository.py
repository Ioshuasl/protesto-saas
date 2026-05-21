from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.g_cidade import get_g_cidade_model
from packages.v1.administrativo.schemas.g_cidade_schema import GCidadeSaveSchema


class SaveRepository(BaseRepository):
    def execute(self, g_cidade_schema: GCidadeSaveSchema):
        if use_orm_firebird():
            return self._execute_orm(g_cidade_schema)
        return self._execute_sql(g_cidade_schema)

    def _execute_orm(self, g_cidade_schema: GCidadeSaveSchema) -> dict[str, Any]:
        payload = {
            "CIDADE_ID": g_cidade_schema.cidade_id,
            "UF": g_cidade_schema.uf,
            "CIDADE_NOME": g_cidade_schema.cidade_nome,
            "CODIGO_IBGE": g_cidade_schema.codigo_ibge,
            "CODIGO_GYN": g_cidade_schema.codigo_gyn,
        }
        created = get_g_cidade_model().create(payload)
        return self._map_row(created) or {}

    def _execute_sql(self, g_cidade_schema: GCidadeSaveSchema) -> dict[str, Any]:
        try:
            sql = """
            INSERT INTO G_CIDADE (
                CIDADE_ID,
                UF,
                CIDADE_NOME,
                CODIGO_IBGE,
                CODIGO_GYN
            ) VALUES (
                :cidade_id,
                :uf,
                :cidade_nome,
                :codigo_ibge,
                :codigo_gyn
            )
            RETURNING
                CIDADE_ID,
                UF,
                CIDADE_NOME,
                CODIGO_IBGE,
                CODIGO_GYN;
            """
            params = {
                "cidade_id": g_cidade_schema.cidade_id,
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
                detail=f"Erro ao salvar G_CIDADE: {exc}",
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
