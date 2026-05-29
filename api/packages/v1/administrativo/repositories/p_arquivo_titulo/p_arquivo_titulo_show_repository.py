from __future__ import annotations

from typing import Any, Mapping, Optional

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_arquivo_titulo import get_p_arquivo_titulo_model
from packages.v1.administrativo.model.p_titulo import get_p_titulo_model
from packages.v1.administrativo.repositories.p_arquivo_titulo.p_arquivo_titulo_index_repository import (
    _SELECT_ATTRIBUTES,
    _SELECT_COLUMNS,
)
from packages.v1.administrativo.repositories.p_arquivo_titulo.p_arquivo_titulo_orm_helpers import (
    _ARQUIVO_TITULO_TITULOS_INCLUDE,
)
from packages.v1.administrativo.schemas.p_arquivo_titulo_schema import (
    PArquivoTituloShowSchema,
    map_arquivo_titulo_row,
)
from packages.v1.administrativo.schemas.p_titulo_schema import map_titulo_row


class ShowRepository(BaseRepository):
    def execute(self, arquivo_schema: PArquivoTituloShowSchema) -> dict[str, Any]:
        if use_orm_firebird():
            return self._execute_orm(arquivo_schema)
        return self._execute_sql(arquivo_schema)

    def _execute_orm(self, arquivo_schema: PArquivoTituloShowSchema) -> dict[str, Any]:
        options: dict[str, Any] = {
            "attributes": _SELECT_ATTRIBUTES,
            "where": {"ARQUIVO_TITULO_ID": arquivo_schema.arquivo_titulo_id},
        }
        if "titulos" in arquivo_schema.includes:
            options["include"] = _ARQUIVO_TITULO_TITULOS_INCLUDE

        row = get_p_arquivo_titulo_model().findOne(options)
        return self._map_show_row(row, arquivo_schema)

    def _execute_sql(self, arquivo_schema: PArquivoTituloShowSchema) -> dict[str, Any]:
        sql = f"""
        SELECT
            {_SELECT_COLUMNS.strip()}
        FROM P_ARQUIVO_TITULO
        WHERE ARQUIVO_TITULO_ID = :arquivo_titulo_id
        """
        row = self.fetch_one(
            sql, {"arquivo_titulo_id": arquivo_schema.arquivo_titulo_id}
        )
        return self._map_show_row(row, arquivo_schema)

    def _map_show_row(
        self,
        row: Optional[Mapping[str, Any]],
        arquivo_schema: PArquivoTituloShowSchema,
    ) -> dict[str, Any]:
        if row is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Arquivo de título não encontrado.",
            )

        row_dict = dict(row)
        titulos_raw = row_dict.pop("titulos", None) or row_dict.pop("TITULOS", None)

        result = map_arquivo_titulo_row(row_dict)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Arquivo de título não encontrado.",
            )

        if "titulos" in arquivo_schema.includes:
            if titulos_raw is None:
                titulos_raw = self._load_titulos_sql(arquivo_schema.arquivo_titulo_id)
            result["titulos"] = self._map_titulos_list(titulos_raw)

        return result

    def _load_titulos_sql(self, arquivo_titulo_id: int) -> list[Mapping[str, Any]]:
        rows = get_p_titulo_model().findAll(
            {
                "where": {"ARQUIVO_TITULO_ID": arquivo_titulo_id},
                "order": [("TITULO_ID", "ASC")],
            }
        )
        return list(rows or [])

    @staticmethod
    def _map_titulos_list(rows: Any) -> list[dict[str, Any]]:
        if not isinstance(rows, list):
            return []
        mapped: list[dict[str, Any]] = []
        for item in rows:
            titulo = map_titulo_row(item)
            if titulo:
                mapped.append(titulo)
        return mapped
