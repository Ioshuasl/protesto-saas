from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.g_sistema import get_g_sistema_model
from packages.v1.administrativo.schemas.g_sistema_schema import GSistemaIdSchema

SITUACAO_CODIGO_INATIVO = "I"


class ShowRepository(BaseRepository):
    def execute(self, sistema_schema: GSistemaIdSchema):
        if use_orm_firebird():
            return self._execute_orm(sistema_schema)
        return self._execute_sql(sistema_schema)

    def _execute_orm(self, sistema_schema: GSistemaIdSchema) -> dict[str, Any]:
        row = get_g_sistema_model().findByPk(sistema_schema.sistema_id)
        result = self._map_sistema_row(row)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registro não encontrado",
            )
        return result

    def _execute_sql(self, sistema_schema: GSistemaIdSchema) -> dict[str, Any]:
        try:
            sql = """
            SELECT
                SISTEMA_ID,
                DESCRICAO,
                SITUACAO,
                TIPO_CARTORIO,
                VERSAO,
                DATA_VERSAO,
                NOME_EXE
            FROM G_SISTEMA
            WHERE SISTEMA_ID = :sistema_id
            """
            params = {"sistema_id": sistema_schema.sistema_id}
            result = self.fetch_one(sql, params)

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Registro não encontrado",
                )

            return self._map_sistema_row(result)
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao buscar sistema: {exc}",
            ) from exc

    @staticmethod
    def _map_sistema_row(row: Optional[Mapping[str, Any]]) -> Optional[dict[str, Any]]:
        mapped = normalize_row_keys(row)
        if mapped is None:
            return None

        sistema_id = mapped.get("sistema_id")
        if isinstance(sistema_id, Decimal):
            mapped["sistema_id"] = (
                int(sistema_id) if sistema_id == sistema_id.to_integral_value() else float(sistema_id)
            )

        situacao = mapped.get("situacao")
        if situacao is None or not str(situacao).strip():
            mapped["situacao"] = SITUACAO_CODIGO_INATIVO
        else:
            mapped["situacao"] = str(situacao).strip().upper()

        tipo_cartorio = mapped.get("tipo_cartorio")
        if tipo_cartorio is not None:
            mapped["tipo_cartorio"] = str(tipo_cartorio).strip() or None

        return mapped
