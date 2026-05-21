from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_livro_natureza import get_p_livro_natureza_model
from packages.v1.administrativo.schemas.p_livro_natureza_schema import (
    PLivroNaturezaIdSchema,
    normalize_sigla_from_db,
    situacao_from_db,
)

_SELECT_COLUMNS = """
    LIVRO_NATUREZA_ID,
    SIGLA,
    DESCRICAO,
    SITUACAO
"""


class ShowRepository(BaseRepository):
    def execute(self, livro_natureza_schema: PLivroNaturezaIdSchema):
        if use_orm_firebird():
            return self._execute_orm(livro_natureza_schema)
        return self._execute_sql(livro_natureza_schema)

    def _execute_orm(
        self, livro_natureza_schema: PLivroNaturezaIdSchema
    ) -> Optional[dict[str, Any]]:
        row = get_p_livro_natureza_model().findByPk(
            livro_natureza_schema.livro_natureza_id
        )
        return self._map_livro_natureza_row(row)

    def _execute_sql(
        self, livro_natureza_schema: PLivroNaturezaIdSchema
    ) -> Optional[dict[str, Any]]:
        sql = f"""
        SELECT
            {_SELECT_COLUMNS.strip()}
        FROM P_LIVRO_NATUREZA
        WHERE LIVRO_NATUREZA_ID = :livro_natureza_id
        """
        row = self.fetch_one(
            sql, {"livro_natureza_id": livro_natureza_schema.livro_natureza_id}
        )
        return self._map_livro_natureza_row(row)

    @staticmethod
    def _map_livro_natureza_row(
        row: Optional[Mapping[str, Any]],
    ) -> Optional[dict[str, Any]]:
        mapped = normalize_row_keys(row)
        if mapped is None:
            return None

        livro_natureza_id = mapped.get("livro_natureza_id")
        if isinstance(livro_natureza_id, Decimal):
            mapped["livro_natureza_id"] = int(livro_natureza_id)

        mapped["sigla"] = normalize_sigla_from_db(mapped.get("sigla"))

        descricao = mapped.get("descricao")
        if descricao is not None:
            mapped["descricao"] = str(descricao).strip() or None

        mapped["situacao"] = situacao_from_db(mapped.get("situacao"))
        mapped.pop("tipo", None)
        mapped.pop("natureza_id", None)

        return mapped
