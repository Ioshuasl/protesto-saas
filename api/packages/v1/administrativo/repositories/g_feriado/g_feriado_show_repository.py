from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.g_feriado import get_g_feriado_model
from packages.v1.administrativo.schemas.g_feriado_schema import GFeriadoIdSchema

SITUACAO_CODIGO_INATIVO = "I"


class ShowRepository(BaseRepository):
    def execute(self, feriado_schema: GFeriadoIdSchema):
        if use_orm_firebird():
            return self._execute_orm(feriado_schema)
        return self._execute_sql(feriado_schema)

    def _execute_orm(self, feriado_schema: GFeriadoIdSchema) -> dict[str, Any]:
        row = get_g_feriado_model().findByPk(feriado_schema.feriado_id)
        result = self._map_feriado_row(row)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registro não encontrado",
            )
        return result

    def _execute_sql(self, feriado_schema: GFeriadoIdSchema) -> dict[str, Any]:
        try:
            sql = """
            SELECT
                FERIADO_ID,
                ANO,
                MES,
                DIA,
                DATA,
                DESCRICAO,
                TIPO,
                SITUACAO
            FROM G_FERIADO
            WHERE FERIADO_ID = :feriado_id
            """
            params = {"feriado_id": feriado_schema.feriado_id}
            result = self.fetch_one(sql, params)

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Registro não encontrado",
                )

            return self._map_feriado_row(result)
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao buscar feriado: {exc}",
            ) from exc

    @staticmethod
    def _map_feriado_row(row: Optional[Mapping[str, Any]]) -> Optional[dict[str, Any]]:
        mapped = normalize_row_keys(row)
        if mapped is None:
            return None

        feriado_id = mapped.get("feriado_id")
        if isinstance(feriado_id, Decimal):
            mapped["feriado_id"] = int(feriado_id)

        for key in ("ano", "mes", "dia"):
            value = mapped.get(key)
            if isinstance(value, Decimal):
                mapped[key] = int(value)

        tipo = mapped.get("tipo")
        if tipo is not None:
            mapped["tipo"] = str(tipo).strip().upper() or None

        situacao = mapped.get("situacao")
        if situacao is None or not str(situacao).strip():
            mapped["situacao"] = SITUACAO_CODIGO_INATIVO
        else:
            mapped["situacao"] = str(situacao).strip().upper()

        return mapped
