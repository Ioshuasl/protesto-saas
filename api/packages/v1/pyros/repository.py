from packages.v1.pyros.builders.write_builders import (
    DeleteBuilder,
    InsertBuilder,
    UpsertBuilder,
    UpdateBuilder,
)
from packages.v1.pyros.builders.select_builder import SelectBuilder


class PyrosRepository:
    table: str = ""
    alias: str | None = None
    allowed_fields: dict[str, str] = {}

    @classmethod
    def select(cls, fields: list[str] | None = None) -> SelectBuilder:
        builder = SelectBuilder(
            table=cls.table,
            alias=cls.alias,
            allowed_fields=cls.allowed_fields,
        )
        return builder.select(fields)

    @classmethod
    def insert(cls, payload: dict[str, object]) -> InsertBuilder:
        return InsertBuilder(table=cls.table, allowed_fields=cls.allowed_fields, payload=payload)

    @classmethod
    def insert_many(cls, payloads: list[dict[str, object]]) -> InsertBuilder:
        return InsertBuilder(
            table=cls.table,
            allowed_fields=cls.allowed_fields,
            payloads=tuple(payloads),
        )

    @classmethod
    def update(cls, payload: dict[str, object]) -> UpdateBuilder:
        return UpdateBuilder(table=cls.table, allowed_fields=cls.allowed_fields).set_payload(payload)

    @classmethod
    def delete(cls) -> DeleteBuilder:
        return DeleteBuilder(table=cls.table, allowed_fields=cls.allowed_fields)

    @classmethod
    def upsert(cls, payload: dict[str, object]) -> UpsertBuilder:
        return UpsertBuilder(table=cls.table, allowed_fields=cls.allowed_fields, payload=payload)
