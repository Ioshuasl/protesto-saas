from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from packages.v1.administrativo.schemas.p_certidao_schema import (
    PCertidaoConsultaApresentanteSchema,
)

_CPFCNPJ_STRIP_CHARS = ".-/ \\(),"


def _digits_only(value: str | None) -> str:
    return "".join(ch for ch in str(value or "") if ch.isdigit())


def _normalized_text(value: str | None) -> str:
    return " ".join(str(value or "").strip().lower().split())


def _normalized_cpfcnpj_sql(alias: str, column: str) -> str:
    expr = f"TRIM(COALESCE({alias}.{column}, ''))"
    for char in _CPFCNPJ_STRIP_CHARS:
        expr = f"REPLACE({expr}, '{char}', '')"
    return expr


def _effective_doc_sql() -> str:
    vinculo_doc = _normalized_cpfcnpj_sql("v", "CPFCNPJ")
    pessoa_doc = _normalized_cpfcnpj_sql("p", "CPFCNPJ")
    return f"COALESCE(NULLIF({vinculo_doc}, ''), {pessoa_doc})"


def _effective_name_sql() -> str:
    return "COALESCE(NULLIF(TRIM(v.NOME), ''), TRIM(p.NOME))"


_SELECT_COLUMNS = f"""
    t.TITULO_ID,
    t.DATA_APONTAMENTO,
    t.DATA_INTIMACAO,
    t.DATA_PROTESTO,
    t.DATA_PAGO,
    t.DATA_CANCELAMENTO,
    t.NUMERO_TITULO,
    t.NUMERO_APONTAMENTO,
    t.VALOR_TITULO,
    v.PESSOA_VINCULO_ID,
    v.TIPO_VINCULO,
    {_effective_name_sql()} AS DEVEDOR_NOME,
    {_effective_doc_sql()} AS DEVEDOR_CPFCNPJ,
    (
        SELECT FIRST 1 vc.NOME
        FROM P_PESSOA_VINCULO vc
        WHERE vc.TITULO_ID = t.TITULO_ID
          AND UPPER(TRIM(vc.TIPO_VINCULO)) = 'CREDOR'
        ORDER BY vc.PESSOA_VINCULO_ID
    ) AS CREDOR_NOME
"""


class ConsultaApresentanteRepository(BaseRepository):
    def execute(
        self, schema: PCertidaoConsultaApresentanteSchema
    ) -> dict[str, list[dict[str, Any]]]:
        document_rows = self._fetch_rows_by_document(schema)
        document_rows = self._dedupe_by_titulo_id(document_rows)
        document_ids = {
            row["titulo_id"] for row in document_rows if row.get("titulo_id") is not None
        }

        homonym_rows = [
            row
            for row in self._dedupe_by_titulo_id(self._fetch_rows_by_name(schema))
            if row.get("titulo_id") not in document_ids
        ]

        return {
            "titulosPorDocumento": document_rows,
            "candidatosHomonimia": homonym_rows,
        }

    def _fetch_rows_by_document(
        self, schema: PCertidaoConsultaApresentanteSchema
    ) -> list[dict[str, Any]]:
        cpfcnpj_digits = _digits_only(schema.cpfcnpj)
        if not cpfcnpj_digits:
            return []

        where, params = self._base_filters(schema)
        where.append(f"{_effective_doc_sql()} = :cpfcnpj")
        params["cpfcnpj"] = cpfcnpj_digits
        return self._fetch_rows(where, params)

    def _fetch_rows_by_name(
        self, schema: PCertidaoConsultaApresentanteSchema
    ) -> list[dict[str, Any]]:
        apresentante = schema.apresentante.strip()
        if not apresentante:
            return []

        cpfcnpj_digits = _digits_only(schema.cpfcnpj)
        where, params = self._base_filters(schema)
        where.append(f"UPPER({_effective_name_sql()}) LIKE UPPER(:apresentante)")
        params["apresentante"] = f"%{apresentante}%"

        if cpfcnpj_digits:
            doc_sql = _effective_doc_sql()
            where.append(f"({doc_sql} IS NULL OR {doc_sql} = '' OR {doc_sql} <> :cpfcnpj)")
            params["cpfcnpj"] = cpfcnpj_digits

        return [
            row
            for row in self._fetch_rows(where, params)
            if _normalized_text(row.get("devedor_nome")).find(
                _normalized_text(schema.apresentante)
            )
            >= 0
        ]

    def _base_filters(
        self, schema: PCertidaoConsultaApresentanteSchema
    ) -> tuple[list[str], dict[str, Any]]:
        where = [
            "t.DATA_PROTESTO IS NOT NULL",
        ]
        params: dict[str, Any] = {}

        if schema.data_inicio is not None:
            where.append("CAST(t.DATA_PROTESTO AS DATE) >= :data_inicio")
            params["data_inicio"] = schema.data_inicio

        data_fim = schema.data_fim or schema.data_inicio
        if data_fim is not None:
            where.append("CAST(t.DATA_PROTESTO AS DATE) <= :data_fim")
            params["data_fim"] = data_fim

        return where, params

    def _fetch_rows(
        self, where: list[str], params: dict[str, Any]
    ) -> list[dict[str, Any]]:
        sql = f"""
        SELECT
            {_SELECT_COLUMNS.strip()}
        FROM P_PESSOA_VINCULO v
        INNER JOIN P_TITULO t ON t.TITULO_ID = v.TITULO_ID
        LEFT JOIN P_PESSOA p ON p.PESSOA_ID = v.PESSOA_ID
        WHERE {" AND ".join(where)}
        ORDER BY t.DATA_PROTESTO DESC, t.TITULO_ID DESC, v.PESSOA_VINCULO_ID ASC
        """
        rows = self.fetch_all(sql, params)
        return [self._map_row(row) for row in rows]

    @classmethod
    def _dedupe_by_titulo_id(
        cls, rows: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        seen: set[int] = set()
        result: list[dict[str, Any]] = []

        for row in rows:
            titulo_id = row.get("titulo_id")
            if titulo_id is None:
                continue
            if int(titulo_id) in seen:
                continue
            seen.add(int(titulo_id))
            result.append(row)

        return result

    @classmethod
    def _map_row(cls, row: Mapping[str, Any]) -> dict[str, Any]:
        mapped = normalize_row_keys(row) or {}

        for key in (
            "titulo_id",
            "pessoa_vinculo_id",
        ):
            mapped[key] = cls._int_or_original(mapped.get(key))

        for key in (
            "numero_apontamento",
            "valor_titulo",
        ):
            mapped[key] = cls._float_or_original(mapped.get(key))

        for key in (
            "numero_titulo",
            "tipo_vinculo",
            "devedor_nome",
            "devedor_cpfcnpj",
            "credor_nome",
        ):
            value = mapped.get(key)
            if value is not None:
                mapped[key] = str(value).strip() or None

        mapped["status_descricao"] = cls._resolve_status_descricao(mapped)
        mapped["vinculos_partes"] = [
            {
                "pessoa_vinculo_id": mapped.get("pessoa_vinculo_id"),
                "tipo": str(mapped.get("tipo_vinculo") or ""),
                "descricao": str(mapped.get("tipo_vinculo") or ""),
                "nome": mapped.get("devedor_nome"),
                "cpfcnpj": mapped.get("devedor_cpfcnpj"),
            }
        ]
        return mapped

    @staticmethod
    def _resolve_status_descricao(row: Mapping[str, Any]) -> str:
        if row.get("data_cancelamento") is not None:
            return "Cancelado"
        if row.get("data_pago") is not None:
            return "Pago"
        return "Protestado"

    @staticmethod
    def _int_or_original(value: Any) -> Any:
        if value is None:
            return None
        if isinstance(value, Decimal):
            return int(value)
        if isinstance(value, str):
            try:
                decimal_value = Decimal(value)
            except Exception:
                return value
            if decimal_value == decimal_value.to_integral_value():
                return int(decimal_value)
        return value

    @staticmethod
    def _float_or_original(value: Any) -> Any:
        if value is None:
            return None
        if isinstance(value, Decimal):
            return float(value)
        if isinstance(value, str):
            try:
                return float(Decimal(value))
            except Exception:
                return value
        return value
