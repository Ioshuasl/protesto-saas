from dataclasses import dataclass, field, replace
from typing import Any

from packages.v1.pyros.exceptions.errors import PyrosSecurityError, PyrosValidationError


def _normalize_column(mapped_field: str) -> str:
    if "." in mapped_field:
        return mapped_field.split(".")[-1]
    return mapped_field


@dataclass(frozen=True, slots=True)
class _WhereClause:
    field: str
    operator: str
    value: Any
    connector: str = "and"


@dataclass(frozen=True, slots=True)
class _WriteState:
    payload: dict[str, Any] = field(default_factory=dict)
    payloads: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    where: tuple[_WhereClause, ...] = field(default_factory=tuple)
    returning: tuple[str, ...] = field(default_factory=tuple)
    allow_full_table_operation: bool = False


class _BaseWriteBuilder:
    def __init__(self, table: str, allowed_fields: dict[str, str]) -> None:
        self._table = table
        self._allowed_fields = dict(allowed_fields)

    def _resolve_column(self, field: str) -> str:
        try:
            mapped = self._allowed_fields[field]
        except KeyError as exc:
            raise PyrosValidationError(f"Campo nao permitido: {field}") from exc
        return _normalize_column(mapped)

    def _normalize_operator(self, value: Any) -> tuple[str, Any]:
        operator = getattr(value, "operator", "=")
        operator_value = getattr(value, "value", value)
        return operator, operator_value

    def _compile_where(
        self,
        where_clauses: tuple[_WhereClause, ...],
        start_param_name: str = "p_where",
    ) -> tuple[str, dict[str, Any]]:
        if not where_clauses:
            return "", {}

        parts: list[str] = []
        params: dict[str, Any] = {}
        for index, clause in enumerate(where_clauses, start=1):
            column = self._resolve_column(clause.field)
            param_name = f"{start_param_name}_{index}"
            rendered = f"{column} {clause.operator} :{param_name}"
            if parts:
                parts.append(clause.connector.upper())
            parts.append(rendered)
            params[param_name] = clause.value

        return f"WHERE {' '.join(parts)}", params


class InsertBuilder(_BaseWriteBuilder):
    def __init__(
        self,
        table: str,
        allowed_fields: dict[str, str],
        payload: dict[str, Any] | None = None,
        payloads: tuple[dict[str, Any], ...] | None = None,
    ) -> None:
        super().__init__(table=table, allowed_fields=allowed_fields)
        self._payload = payload or {}
        self._payloads = payloads or tuple()

    def compile(self) -> tuple[str, dict[str, Any]]:
        if self._payload:
            return self._compile_one(self._payload)
        return self._compile_many(self._payloads)

    def _compile_one(self, payload: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        if not payload:
            raise PyrosValidationError("Payload de insert nao pode ser vazio")

        columns: list[str] = []
        placeholders: list[str] = []
        params: dict[str, Any] = {}

        for index, (field, value) in enumerate(payload.items(), start=1):
            columns.append(self._resolve_column(field))
            param_name = f"p_{index}"
            placeholders.append(f":{param_name}")
            params[param_name] = value

        sql = (
            f"INSERT INTO {self._table} ({', '.join(columns)}) "
            f"VALUES ({', '.join(placeholders)})"
        )
        return sql, params

    def _compile_many(
        self, payloads: tuple[dict[str, Any], ...]
    ) -> tuple[str, dict[str, Any]]:
        if not payloads:
            raise PyrosValidationError("Payloads de insert_many nao podem ser vazios")

        first = payloads[0]
        if not first:
            raise PyrosValidationError("Payload de insert_many nao pode ser vazio")

        fields = tuple(first.keys())
        columns = [self._resolve_column(field) for field in fields]
        params: dict[str, Any] = {}
        rows: list[str] = []

        for row_index, payload in enumerate(payloads, start=1):
            if tuple(payload.keys()) != fields:
                raise PyrosValidationError(
                    "Todos os payloads devem ter os mesmos campos"
                )

            placeholders: list[str] = []
            for col_index, field in enumerate(fields, start=1):
                param_name = f"p_{row_index}_{col_index}"
                placeholders.append(f":{param_name}")
                params[param_name] = payload[field]

            rows.append(f"({', '.join(placeholders)})")

        sql = (
            f"INSERT INTO {self._table} ({', '.join(columns)}) VALUES {', '.join(rows)}"
        )
        return sql, params


class UpdateBuilder(_BaseWriteBuilder):
    def __init__(
        self,
        table: str,
        allowed_fields: dict[str, str],
        state: _WriteState | None = None,
    ) -> None:
        super().__init__(table=table, allowed_fields=allowed_fields)
        self._state = state or _WriteState()

    def _clone(self, state: _WriteState) -> "UpdateBuilder":
        return UpdateBuilder(
            table=self._table, allowed_fields=self._allowed_fields, state=state
        )

    def set_payload(self, payload: dict[str, Any]) -> "UpdateBuilder":
        if not payload:
            raise PyrosValidationError("Payload de update nao pode ser vazio")

        for field in payload:
            self._resolve_column(field)
        return self._clone(replace(self._state, payload=dict(payload)))

    def where(self, filters: dict[str, Any]) -> "UpdateBuilder":
        clauses = list(self._state.where)
        for field, raw_value in filters.items():
            self._resolve_column(field)
            operator, value = self._normalize_operator(raw_value)
            clauses.append(
                _WhereClause(
                    field=field, operator=operator, value=value, connector="and"
                )
            )
        return self._clone(replace(self._state, where=tuple(clauses)))

    def returning(self, fields: list[str]) -> "UpdateBuilder":
        if not fields:
            raise PyrosValidationError("Campos de returning nao podem ser vazios")
        for field in fields:
            self._resolve_column(field)
        return self._clone(replace(self._state, returning=tuple(fields)))

    def unsafe_allow_full_table_operation(self) -> "UpdateBuilder":
        return self._clone(replace(self._state, allow_full_table_operation=True))

    def compile(self) -> tuple[str, dict[str, Any]]:
        if not self._state.payload:
            raise PyrosValidationError("Payload de update nao pode ser vazio")
        if not self._state.where and not self._state.allow_full_table_operation:
            raise PyrosSecurityError("UPDATE sem WHERE bloqueado por seguranca")

        set_parts: list[str] = []
        params: dict[str, Any] = {}

        for index, (field, value) in enumerate(self._state.payload.items(), start=1):
            column = self._resolve_column(field)
            param_name = f"p_set_{index}"
            set_parts.append(f"{column} = :{param_name}")
            params[param_name] = value

        where_sql, where_params = self._compile_where(self._state.where)
        params.update(where_params)

        sql = f"UPDATE {self._table} SET {', '.join(set_parts)}"
        if where_sql:
            sql = f"{sql} {where_sql}"

        if self._state.returning:
            returning_columns = ", ".join(
                self._resolve_column(field) for field in self._state.returning
            )
            sql = f"{sql} RETURNING {returning_columns}"

        return sql, params


class DeleteBuilder(_BaseWriteBuilder):
    def __init__(
        self,
        table: str,
        allowed_fields: dict[str, str],
        state: _WriteState | None = None,
    ) -> None:
        super().__init__(table=table, allowed_fields=allowed_fields)
        self._state = state or _WriteState()

    def _clone(self, state: _WriteState) -> "DeleteBuilder":
        return DeleteBuilder(
            table=self._table, allowed_fields=self._allowed_fields, state=state
        )

    def where(self, filters: dict[str, Any]) -> "DeleteBuilder":
        clauses = list(self._state.where)
        for field, raw_value in filters.items():
            self._resolve_column(field)
            operator, value = self._normalize_operator(raw_value)
            clauses.append(
                _WhereClause(
                    field=field, operator=operator, value=value, connector="and"
                )
            )
        return self._clone(replace(self._state, where=tuple(clauses)))

    def unsafe_allow_full_table_operation(self) -> "DeleteBuilder":
        return self._clone(replace(self._state, allow_full_table_operation=True))

    def compile(self) -> tuple[str, dict[str, Any]]:
        if not self._state.where and not self._state.allow_full_table_operation:
            raise PyrosSecurityError("DELETE sem WHERE bloqueado por seguranca")

        where_sql, params = self._compile_where(self._state.where)
        sql = f"DELETE FROM {self._table}"
        if where_sql:
            sql = f"{sql} {where_sql}"
        return sql, params


class UpsertBuilder(_BaseWriteBuilder):
    def __init__(
        self,
        table: str,
        allowed_fields: dict[str, str],
        payload: dict[str, Any],
        matching_fields: tuple[str, ...] | None = None,
    ) -> None:
        super().__init__(table=table, allowed_fields=allowed_fields)
        self._payload = dict(payload)
        self._matching_fields = matching_fields or tuple()

    def matching(self, fields: list[str]) -> "UpsertBuilder":
        if not fields:
            raise PyrosValidationError("Campos de matching nao podem ser vazios")
        for field in fields:
            self._resolve_column(field)
        return UpsertBuilder(
            table=self._table,
            allowed_fields=self._allowed_fields,
            payload=self._payload,
            matching_fields=tuple(fields),
        )

    def compile(self) -> tuple[str, dict[str, Any]]:
        if not self._payload:
            raise PyrosValidationError("Payload de upsert nao pode ser vazio")
        if not self._matching_fields:
            raise PyrosValidationError("Upsert exige campos de matching")

        columns: list[str] = []
        placeholders: list[str] = []
        params: dict[str, Any] = {}

        for index, (field, value) in enumerate(self._payload.items(), start=1):
            column = self._resolve_column(field)
            param_name = f"p_{index}"
            columns.append(column)
            placeholders.append(f":{param_name}")
            params[param_name] = value

        matching = ", ".join(
            self._resolve_column(field) for field in self._matching_fields
        )
        sql = (
            f"UPDATE OR INSERT INTO {self._table} ({', '.join(columns)}) "
            f"VALUES ({', '.join(placeholders)}) MATCHING ({matching})"
        )
        return sql, params
