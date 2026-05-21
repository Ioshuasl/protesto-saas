from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_livro_andamento import get_p_livro_andamento_model
from packages.v1.administrativo.schemas.p_livro_andamento_schema import (
    PLivroAndamentoIdSchema,
    is_livro_aberto,
    normalize_sigla,
)

_SELECT_COLUMNS = """
    LIVRO_ANDAMENTO_ID,
    LIVRO_NATUREZA_ID,
    FOLHA_ATUAL,
    NUMERO_LIVRO,
    NUMERO_LIVRO_LETRA,
    DATA_ABERTURA,
    DATA_FECHAMENTO,
    NUMERO_FOLHAS,
    SIGLA,
    USUARIO_ID
"""


class ShowRepository(BaseRepository):
    def execute(self, livro_andamento_schema: PLivroAndamentoIdSchema):
        if use_orm_firebird():
            return self._execute_orm(livro_andamento_schema)
        return self._execute_sql(livro_andamento_schema)

    def _execute_orm(
        self, livro_andamento_schema: PLivroAndamentoIdSchema
    ) -> Optional[dict[str, Any]]:
        row = get_p_livro_andamento_model().findByPk(
            livro_andamento_schema.livro_andamento_id
        )
        return self._map_livro_andamento_row(row)

    def _execute_sql(
        self, livro_andamento_schema: PLivroAndamentoIdSchema
    ) -> Optional[dict[str, Any]]:
        sql = f"""
        SELECT {_SELECT_COLUMNS.strip()}
        FROM P_LIVRO_ANDAMENTO
        WHERE LIVRO_ANDAMENTO_ID = :livro_andamento_id
        """
        row = self.fetch_one(
            sql, {"livro_andamento_id": livro_andamento_schema.livro_andamento_id}
        )
        return self._map_livro_andamento_row(row)

    @staticmethod
    def _map_livro_andamento_row(
        row: Optional[Mapping[str, Any]],
    ) -> Optional[dict[str, Any]]:
        mapped = normalize_row_keys(row)
        if mapped is None:
            return None

        for key in (
            "livro_andamento_id",
            "livro_natureza_id",
            "folha_atual",
            "numero_livro",
            "numero_folhas",
            "usuario_id",
        ):
            val = mapped.get(key)
            if isinstance(val, Decimal):
                mapped[key] = int(val)

        sigla = mapped.get("sigla")
        if sigla is not None:
            mapped["sigla"] = normalize_sigla(str(sigla))

        mapped["aberto"] = is_livro_aberto(mapped.get("data_fechamento"))
        mapped.pop("numero_livro_letra", None)

        return mapped
