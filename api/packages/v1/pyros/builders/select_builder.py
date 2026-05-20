from dataclasses import replace
from typing import Any, Iterator, Mapping

from packages.v1.pyros.compiler.firebird_compiler import FirebirdCompiler
from packages.v1.pyros.exceptions.errors import PyrosSecurityError, PyrosValidationError
from packages.v1.pyros.schemas.query_models import (
    FilterClause,
    JoinClause,
    OrderClause,
    RawClause,
    SelectQuery,
)


class SelectBuilder:
    def __init__(
        self,
        table: str,
        alias: str | None,
        allowed_fields: dict[str, str],
        query: SelectQuery | None = None,
    ) -> None:
        self._table = table
        self._alias = alias
        self._allowed_fields = dict(allowed_fields)
        self._query = query or SelectQuery(table=table, alias=alias)

    def _clone(self, query: SelectQuery) -> "SelectBuilder":
        return SelectBuilder(
            table=self._table,
            alias=self._alias,
            allowed_fields=self._allowed_fields,
            query=query,
        )

    def _resolve_field(self, field: str) -> str:
        try:
            return self._allowed_fields[field]
        except KeyError as exc:
            raise PyrosValidationError(f"Campo nao permitido: {field}") from exc

    def _normalize_operator(self, value: Any) -> tuple[str, Any]:
        operator = getattr(value, "operator", "=")
        operator_value = getattr(value, "value", value)
        return operator, operator_value

    def select(self, fields: list[str] | None = None) -> "SelectBuilder":
        if fields is None:
            field_names = tuple(self._allowed_fields.keys())
        else:
            field_names = tuple(fields)
            for field_name in field_names:
                self._resolve_field(field_name)

        return self._clone(replace(self._query, fields=field_names))

    def where(self, filters: dict[str, Any]) -> "SelectBuilder":
        clauses = list(self._query.filters)
        for field_name, raw_value in filters.items():
            self._resolve_field(field_name)
            operator, value = self._normalize_operator(raw_value)
            clauses.append(
                FilterClause(
                    field=field_name,
                    operator=operator,
                    value=value,
                    connector="and",
                )
            )
        return self._clone(replace(self._query, filters=tuple(clauses)))

    def or_where(self, filters: dict[str, Any]) -> "SelectBuilder":
        clauses = list(self._query.filters)
        for field_name, raw_value in filters.items():
            self._resolve_field(field_name)
            operator, value = self._normalize_operator(raw_value)
            clauses.append(
                FilterClause(
                    field=field_name,
                    operator=operator,
                    value=value,
                    connector="or",
                )
            )
        return self._clone(replace(self._query, filters=tuple(clauses)))

    def left_join(self, table: str, on: str, alias: str | None = None) -> "SelectBuilder":
        joins = list(self._query.joins)
        joins.append(JoinClause(join_type="left", table=table, on=on, alias=alias))
        return self._clone(replace(self._query, joins=tuple(joins)))

    def group_by(self, field: str) -> "SelectBuilder":
        self._resolve_field(field)
        grouping = list(self._query.group_by)
        grouping.append(field)
        return self._clone(replace(self._query, group_by=tuple(grouping)))

    def having(self, filters: dict[str, Any]) -> "SelectBuilder":
        clauses = list(self._query.having)
        for field_name, raw_value in filters.items():
            self._resolve_field(field_name)
            operator, value = self._normalize_operator(raw_value)
            clauses.append(
                FilterClause(
                    field=field_name,
                    operator=operator,
                    value=value,
                    connector="and",
                )
            )
        return self._clone(replace(self._query, having=tuple(clauses)))

    def unsafe_allow_raw_sql(self) -> "SelectBuilder":
        return self._clone(replace(self._query, allow_raw_sql=True))

    def where_raw(
        self,
        sql_fragment: str,
        params: dict[str, Any] | None = None,
        connector: str = "and",
    ) -> "SelectBuilder":
        if not self._query.allow_raw_sql:
            raise PyrosSecurityError("Raw SQL bloqueado. Use unsafe_allow_raw_sql() explicitamente.")

        normalized_connector = connector.lower().strip()
        if normalized_connector not in {"and", "or"}:
            raise PyrosValidationError("Conector invalido para where_raw. Use 'and' ou 'or'.")

        raw_clauses = list(self._query.raw_filters)
        raw_clauses.append(
            RawClause(
                sql=sql_fragment.strip(),
                params=tuple((params or {}).items()),
                connector=normalized_connector,  # type: ignore[arg-type]
            )
        )
        return self._clone(replace(self._query, raw_filters=tuple(raw_clauses)))

    def order_by(self, field: str, direction: str = "asc") -> "SelectBuilder":
        self._resolve_field(field)
        normalized = direction.lower()
        if normalized not in {"asc", "desc"}:
            raise PyrosValidationError(f"Direcao invalida para order_by: {direction}")

        ordering = list(self._query.order_by)
        ordering.append(OrderClause(field=field, direction=normalized))  # type: ignore[arg-type]
        return self._clone(replace(self._query, order_by=tuple(ordering)))

    def limit(self, value: int) -> "SelectBuilder":
        if value <= 0:
            raise PyrosValidationError("Limit deve ser maior que zero")
        return self._clone(replace(self._query, limit=value))

    def paginate(self, page: int, per_page: int) -> "SelectBuilder":
        try:
            page_int = int(page)
            per_page_int = int(per_page)
        except (TypeError, ValueError) as exc:
            raise PyrosValidationError(
                "Page e per_page devem ser inteiros validos"
            ) from exc

        if page_int <= 0 or per_page_int <= 0:
            raise PyrosValidationError("Page e per_page devem ser maiores que zero")

        offset = (page_int - 1) * per_page_int
        return self._clone(replace(self._query, limit=per_page_int, offset=offset))

    def count(self) -> "SelectBuilder":
        return self._clone(replace(self._query, is_count=True))

    def compile(self) -> tuple[str, dict[str, Any]]:
        compiler = FirebirdCompiler(allowed_fields=self._allowed_fields)
        compiled = compiler.compile(self._query)
        return compiled.sql, compiled.params

    def to_sql(self) -> str:
        sql, _ = self.compile()
        return sql

    def fetch_all(
        self,
        executor: Any | None = None,
        connection: Any | None = None,
    ) -> list[Mapping[str, Any]]:
        """
        Executa a query diretamente via PyrosExecutor, retornando todas as linhas.

        Permite injetar um executor customizado (para testes) ou usar o executor
        padrão do Pyros quando nenhum for informado.
        """
        from packages.v1.pyros.execution.executor import PyrosExecutor

        sql, params = self.compile()
        real_executor = executor or PyrosExecutor()
        return real_executor.fetch_all(sql, params, connection=connection)

    def stream(
        self,
        executor: Any,
        chunk_size: int = 500,
        connection: Any | None = None,
    ) -> Iterator[Mapping[str, Any]]:
        sql, params = self.compile()
        return executor.stream(sql, params, chunk_size=chunk_size, connection=connection)
