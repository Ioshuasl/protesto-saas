from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.g_feriado import get_g_feriado_model
from packages.v1.administrativo.schemas.g_feriado_schema import GFeriadoUpdateSchema

SITUACAO_CODIGO_INATIVO = "I"


class UpdateRepository(BaseRepository):
    def execute(self, feriado_id: int, feriado_schema: GFeriadoUpdateSchema):
        if use_orm_firebird():
            return self._execute_orm(feriado_id, feriado_schema)
        return self._execute_sql(feriado_id, feriado_schema)

    def _execute_orm(
        self, feriado_id: int, feriado_schema: GFeriadoUpdateSchema
    ) -> dict[str, Any]:
        values: dict[str, Any] = {}

        if feriado_schema.descricao is not None:
            values["DESCRICAO"] = feriado_schema.descricao
        if feriado_schema.tipo is not None:
            values["TIPO"] = feriado_schema.tipo
        if feriado_schema.situacao is not None:
            values["SITUACAO"] = feriado_schema.situacao
        if feriado_schema.data is not None:
            values["DATA"] = feriado_schema.data
        if feriado_schema.ano is not None:
            values["ANO"] = feriado_schema.ano
        if feriado_schema.mes is not None:
            values["MES"] = feriado_schema.mes
        if feriado_schema.dia is not None:
            values["DIA"] = feriado_schema.dia

        model = get_g_feriado_model()
        result = model.update(values, {"where": {"FERIADO_ID": feriado_id}})
        rows = result.get("rows") if isinstance(result, dict) else None
        if rows:
            return self._map_feriado_row(rows[0]) or {}

        return self._map_feriado_row(model.findByPk(feriado_id)) or {}

    def _execute_sql(
        self, feriado_id: int, feriado_schema: GFeriadoUpdateSchema
    ) -> dict[str, Any]:
        try:
            updates = []
            params = {"feriado_id": feriado_id}

            if feriado_schema.descricao is not None:
                updates.append("DESCRICAO = :descricao")
                params["descricao"] = feriado_schema.descricao
            if feriado_schema.tipo is not None:
                updates.append("TIPO = :tipo")
                params["tipo"] = feriado_schema.tipo
            if feriado_schema.situacao is not None:
                updates.append("SITUACAO = :situacao")
                params["situacao"] = feriado_schema.situacao
            if feriado_schema.data is not None:
                updates.append("DATA = :data")
                params["data"] = feriado_schema.data
            if feriado_schema.ano is not None:
                updates.append("ANO = :ano")
                params["ano"] = feriado_schema.ano
            if feriado_schema.mes is not None:
                updates.append("MES = :mes")
                params["mes"] = feriado_schema.mes
            if feriado_schema.dia is not None:
                updates.append("DIA = :dia")
                params["dia"] = feriado_schema.dia

            if not updates:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Nenhum campo informado para atualização.",
                )

            sql = f"""
            UPDATE G_FERIADO
            SET {', '.join(updates)}
            WHERE FERIADO_ID = :feriado_id
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
            result = self.run_and_return(sql, params)

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Feriado não encontrado para atualização.",
                )

            return self._map_feriado_row(result)
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar feriado: {exc}",
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
