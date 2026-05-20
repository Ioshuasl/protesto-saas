from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from orm_py import Op

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.g_feriado import get_g_feriado_model
from packages.v1.administrativo.schemas.g_feriado_schema import GFeriadoIndexSchema

SITUACAO_CODIGO_ATIVO = "A"
SITUACAO_CODIGO_INATIVO = "I"

_SELECT_COLUMNS = """
    FERIADO_ID,
    ANO,
    MES,
    DIA,
    DATA,
    DESCRICAO,
    TIPO,
    SITUACAO
"""


class IndexRepository(BaseRepository):
    def execute(self, feriado_index_schema: GFeriadoIndexSchema):
        if use_orm_firebird():
            return self._execute_orm(feriado_index_schema)
        return self._execute_sql(feriado_index_schema)

    def _execute_orm(self, feriado_index_schema: GFeriadoIndexSchema) -> list[dict[str, Any]]:
        if self._has_string_filters(feriado_index_schema):
            return self._execute_sql(feriado_index_schema)

        where: dict[str, Any] = {}

        if feriado_index_schema.ano is not None:
            where["ANO"] = feriado_index_schema.ano
        if feriado_index_schema.tipo is not None:
            where["TIPO"] = feriado_index_schema.tipo
        if feriado_index_schema.situacao is not None:
            where["SITUACAO"] = feriado_index_schema.situacao
        if feriado_index_schema.descricao is not None:
            where["DESCRICAO"] = {Op.like: f"%{feriado_index_schema.descricao}%"}

        options: dict[str, Any] = {"order": [("DATA", "ASC")]}
        if where:
            options["where"] = where

        rows = get_g_feriado_model().findAll(options)
        return [self._map_feriado_row(row) or {} for row in rows]

    def _execute_sql(self, feriado_index_schema: GFeriadoIndexSchema) -> list[dict[str, Any]]:
        sql = f"""
        SELECT
            {_SELECT_COLUMNS.strip()}
        FROM G_FERIADO
        """
        where: list[str] = []
        params = feriado_index_schema.model_dump(exclude_none=True)

        if feriado_index_schema.ano is not None:
            where.append("ANO = :ano")
        if feriado_index_schema.tipo is not None:
            where.append("UPPER(TIPO) = UPPER(:tipo)")
        if feriado_index_schema.situacao is not None:
            self._append_situacao_filter(where, params, feriado_index_schema.situacao)
        if feriado_index_schema.descricao is not None:
            where.append("UPPER(DESCRICAO) LIKE UPPER(:descricao)")
            params["descricao"] = f"%{feriado_index_schema.descricao}%"

        if where:
            sql += " WHERE " + " AND ".join(where)

        sql += " ORDER BY DATA ASC"
        rows = self.fetch_all(sql, params)
        return [self._map_feriado_row(row) or {} for row in rows]

    @staticmethod
    def _has_string_filters(feriado_index_schema: GFeriadoIndexSchema) -> bool:
        return any(
            [
                feriado_index_schema.tipo is not None,
                feriado_index_schema.situacao is not None,
                feriado_index_schema.descricao is not None,
            ]
        )

    @staticmethod
    def _append_situacao_filter(
        where: list[str], params: dict[str, Any], situacao: str
    ) -> None:
        code = (situacao or "").strip().upper()
        if code == SITUACAO_CODIGO_ATIVO:
            where.append("UPPER(TRIM(SITUACAO)) = 'A'")
        elif code == SITUACAO_CODIGO_INATIVO:
            where.append(
                "(SITUACAO IS NULL OR TRIM(COALESCE(SITUACAO, '')) = '' "
                "OR UPPER(TRIM(SITUACAO)) = 'I')"
            )
        params.pop("situacao", None)

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
