from typing import Any

from packages.v1.pyros.compiler.compiled_query import CompiledQuery
from packages.v1.pyros.exceptions.errors import PyrosCompilationError
from packages.v1.pyros.schemas.query_models import FilterClause, RawClause, SelectQuery


class FirebirdCompiler:
    def __init__(self, allowed_fields: dict[str, str]) -> None:
        self._allowed_fields = dict(allowed_fields)

    def compile(self, query: SelectQuery) -> CompiledQuery:
        if not query.table:
            raise PyrosCompilationError("Tabela da query nao informada")

        select_sql = self._compile_select_clause(query)
        from_sql = self._compile_from_clause(query)
        joins_sql = self._compile_joins_clause(query)
        where_sql, params, next_index = self._compile_filter_clause(
            query.filters, "WHERE", start_index=1
        )
        where_sql, params = self._append_raw_filters(where_sql, params, query.raw_filters)
        group_sql = self._compile_group_by_clause(query)
        having_sql, having_params, _ = self._compile_filter_clause(
            query.having, "HAVING", start_index=next_index
        )
        order_sql = self._compile_order_clause(query)
        rows_sql = self._compile_rows_clause(query)

        params.update(having_params)

        sql_parts = [select_sql, from_sql]
        if joins_sql:
            sql_parts.append(joins_sql)
        if where_sql:
            sql_parts.append(where_sql)
        if group_sql:
            sql_parts.append(group_sql)
        if having_sql:
            sql_parts.append(having_sql)
        if order_sql and not query.is_count:
            sql_parts.append(order_sql)
        if rows_sql and not query.is_count:
            sql_parts.append(rows_sql)

        return CompiledQuery(sql=" ".join(sql_parts), params=params)

    def _append_raw_filters(
        self,
        where_sql: str,
        params: dict[str, Any],
        raw_filters: tuple[RawClause, ...],
    ) -> tuple[str, dict[str, Any]]:
        if not raw_filters:
            return where_sql, params

        where_value = where_sql.removeprefix("WHERE ").strip() if where_sql else ""
        merged_params = dict(params)

        for raw in raw_filters:
            clause = raw.sql.strip()
            if not clause:
                continue

            raw_params = dict(raw.params)
            duplicated = set(merged_params.keys()) & set(raw_params.keys())
            if duplicated:
                duplicated_names = ", ".join(sorted(duplicated))
                raise PyrosCompilationError(
                    f"Conflito de parametros entre filtros e raw SQL: {duplicated_names}"
                )

            if where_value:
                where_value = f"{where_value} {raw.connector.upper()} {clause}"
            else:
                where_value = clause

            merged_params.update(raw_params)

        if not where_value:
            return "", merged_params
        return f"WHERE {where_value}", merged_params

    def _resolve_field(self, field: str) -> str:
        try:
            return self._allowed_fields[field]
        except KeyError as exc:
            raise PyrosCompilationError(f"Campo nao permitido na compilacao: {field}") from exc

    def _compile_select_clause(self, query: SelectQuery) -> str:
        if query.is_count:
            return "SELECT COUNT(*) AS TOTAL"

        fields = query.fields or tuple(self._allowed_fields.keys())
        rendered = ", ".join(self._resolve_field(name) for name in fields)
        return f"SELECT {rendered}"

    def _compile_from_clause(self, query: SelectQuery) -> str:
        if query.alias:
            return f"FROM {query.table} {query.alias}"
        return f"FROM {query.table}"

    def _compile_joins_clause(self, query: SelectQuery) -> str:
        if not query.joins:
            return ""

        parts: list[str] = []
        for join in query.joins:
            join_name = "LEFT JOIN" if join.join_type == "left" else "INNER JOIN"
            alias = f" {join.alias}" if join.alias else ""
            parts.append(f"{join_name} {join.table}{alias} ON {join.on}")
        return " ".join(parts)

    def _compile_filter_clause(
        self,
        clauses: tuple[FilterClause, ...],
        keyword: str,
        start_index: int,
    ) -> tuple[str, dict[str, Any], int]:
        if not clauses:
            return "", {}, start_index

        fragments: list[str] = []
        params: dict[str, Any] = {}
        cursor = start_index

        for clause in clauses:
            field_sql = self._resolve_field(clause.field)
            rendered, new_params, cursor = self._render_filter(field_sql, clause, cursor)
            if fragments:
                fragments.append(clause.connector.upper())
            fragments.append(rendered)
            params.update(new_params)

        return f"{keyword} {' '.join(fragments)}", params, cursor

    def _render_filter(
        self,
        field_sql: str,
        clause: FilterClause,
        cursor: int,
    ) -> tuple[str, dict[str, Any], int]:
        operator = clause.operator.upper()
        params: dict[str, Any] = {}

        if operator == "IS NULL":
            return f"{field_sql} IS NULL", params, cursor

        if operator in {"IN", "NOT IN"}:
            values = clause.value
            if not isinstance(values, (list, tuple)) or not values:
                raise PyrosCompilationError("Operador IN/NOT IN exige lista nao vazia")

            placeholders: list[str] = []
            for item_index, item in enumerate(values, start=1):
                key = f"p_{cursor}_{item_index}"
                placeholders.append(f":{key}")
                params[key] = item
            rendered = f"{field_sql} {operator} ({', '.join(placeholders)})"
            return rendered, params, cursor + 1

        key = f"p_{cursor}"
        params[key] = clause.value
        rendered = f"{field_sql} {operator} :{key}"
        return rendered, params, cursor + 1

    def _compile_group_by_clause(self, query: SelectQuery) -> str:
        if not query.group_by:
            return ""
        fields = [self._resolve_field(item) for item in query.group_by]
        return f"GROUP BY {', '.join(fields)}"

    def _compile_order_clause(self, query: SelectQuery) -> str:
        if not query.order_by:
            return ""
        fields = [
            f"{self._resolve_field(order.field)} {order.direction.upper()}"
            for order in query.order_by
        ]
        return f"ORDER BY {', '.join(fields)}"

    def _compile_rows_clause(self, query: SelectQuery) -> str:
        if query.limit is None:
            return ""
        if query.offset is None:
            return f"ROWS 1 TO {query.limit}"

        start = query.offset + 1
        end = query.offset + query.limit
        return f"ROWS {start} TO {end}"
