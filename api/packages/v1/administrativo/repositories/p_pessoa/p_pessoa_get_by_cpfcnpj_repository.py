from __future__ import annotations

from typing import Any, Optional

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_pessoa import get_p_pessoa_model
from packages.v1.administrativo.schemas.p_pessoa_schema import (
    PPessoaCpfcnpjSchema,
    map_pessoa_row,
)


class GetByCpfcnpjRepository(BaseRepository):
    def execute(self, schema: PPessoaCpfcnpjSchema) -> Optional[dict[str, Any]]:
        if use_orm_firebird():
            return self._execute_orm(schema)
        return self._execute_sql(schema)

    def _execute_orm(self, schema: PPessoaCpfcnpjSchema) -> Optional[dict[str, Any]]:
        where: dict[str, Any] = {"CPFCNPJ": schema.cpfcnpj}
        rows = get_p_pessoa_model().findAll({"where": where, "limit": 5})
        for row in rows or []:
            mapped = map_pessoa_row(row)
            if mapped and self._matches(schema, mapped):
                if schema.pessoa_id is None or mapped.get("pessoa_id") != schema.pessoa_id:
                    return mapped
        return None

    def _execute_sql(self, schema: PPessoaCpfcnpjSchema) -> Optional[dict[str, Any]]:
        sql = """
        SELECT FIRST 5
            PESSOA_ID,
            NOME,
            CPFCNPJ
        FROM P_PESSOA
        WHERE CPFCNPJ IS NOT NULL
          AND TRIM(CPFCNPJ) <> ''
        """
        rows = self.fetch_all(sql, {})
        for row in rows or []:
            mapped = map_pessoa_row(normalize_row_keys(row))
            if mapped and self._matches(schema, mapped):
                if schema.pessoa_id is None or mapped.get("pessoa_id") != schema.pessoa_id:
                    return mapped
        return None

    @staticmethod
    def _matches(schema: PPessoaCpfcnpjSchema, mapped: dict[str, Any]) -> bool:
        stored = mapped.get("cpfcnpj") or ""
        stored_digits = "".join(ch for ch in str(stored) if ch.isdigit())
        return stored_digits == schema.cpfcnpj
