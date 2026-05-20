from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.g_feriado import get_g_feriado_model
from packages.v1.administrativo.schemas.g_feriado_schema import GFeriadoSaveSchema

SITUACAO_CODIGO_INATIVO = "I"


class SaveRepository(BaseRepository):
    def execute(self, feriado_schema: GFeriadoSaveSchema):
        if use_orm_firebird():
            return self._execute_orm(feriado_schema)
        return self._execute_sql(feriado_schema)

    def _execute_orm(self, feriado_schema: GFeriadoSaveSchema) -> dict[str, Any]:
        payload = {
            "FERIADO_ID": feriado_schema.feriado_id,
            "ANO": feriado_schema.ano,
            "MES": feriado_schema.mes,
            "DIA": feriado_schema.dia,
            "DATA": feriado_schema.data,
            "DESCRICAO": feriado_schema.descricao,
            "TIPO": feriado_schema.tipo,
            "SITUACAO": feriado_schema.situacao,
        }
        created = get_g_feriado_model().create(payload)
        return self._map_feriado_row(created) or {}

    def _execute_sql(self, feriado_schema: GFeriadoSaveSchema) -> dict[str, Any]:
        try:
            sql = """
            INSERT INTO G_FERIADO (
                FERIADO_ID,
                ANO,
                MES,
                DIA,
                DATA,
                DESCRICAO,
                TIPO,
                SITUACAO
            ) VALUES (
                :feriado_id,
                :ano,
                :mes,
                :dia,
                :data,
                :descricao,
                :tipo,
                :situacao
            )
            RETURNING
                FERIADO_ID,
                ANO,
                MES,
                DIA,
                DATA,
                DESCRICAO,
                TIPO,
                SITUACAO;
            """
            params = {
                "feriado_id": feriado_schema.feriado_id,
                "ano": feriado_schema.ano,
                "mes": feriado_schema.mes,
                "dia": feriado_schema.dia,
                "data": feriado_schema.data,
                "descricao": feriado_schema.descricao,
                "tipo": feriado_schema.tipo,
                "situacao": feriado_schema.situacao,
            }
            result = self.run_and_return(sql, params)
            return self._map_feriado_row(result)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar feriado: {exc}",
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
