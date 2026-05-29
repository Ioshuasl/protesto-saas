from __future__ import annotations

from typing import Any

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_arquivo_titulo import get_p_arquivo_titulo_model
from packages.v1.administrativo.repositories.p_arquivo_titulo.p_arquivo_titulo_index_repository import (
    _SELECT_ATTRIBUTES,
    _SELECT_COLUMNS,
)
from packages.v1.administrativo.repositories.p_arquivo_titulo.p_arquivo_titulo_save_repository import (
    _FIELD_TO_COLUMN,
)
from packages.v1.administrativo.schemas.p_arquivo_titulo_schema import (
    PArquivoTituloUpdateSchema,
    api_money_to_db,
    map_arquivo_titulo_row,
)


class UpdateRepository(BaseRepository):
    def execute(
        self,
        arquivo_titulo_id: int,
        arquivo_schema: PArquivoTituloUpdateSchema,
    ) -> dict[str, Any]:
        if use_orm_firebird():
            return self._execute_orm(arquivo_titulo_id, arquivo_schema)
        return self._execute_sql(arquivo_titulo_id, arquivo_schema)

    def _execute_orm(
        self,
        arquivo_titulo_id: int,
        arquivo_schema: PArquivoTituloUpdateSchema,
    ) -> dict[str, Any]:
        values = self._build_payload(arquivo_schema)
        if not values:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Nenhum campo informado para atualização.",
            )

        model = get_p_arquivo_titulo_model()
        result = model.update(values, {"where": {"ARQUIVO_TITULO_ID": arquivo_titulo_id}})
        rows = result.get("rows") if isinstance(result, dict) else None
        if rows:
            return map_arquivo_titulo_row(rows[0]) or {}

        row = model.findOne(
            {
                "attributes": _SELECT_ATTRIBUTES,
                "where": {"ARQUIVO_TITULO_ID": arquivo_titulo_id},
            }
        )
        mapped = map_arquivo_titulo_row(row)
        if not mapped:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Arquivo de título não encontrado para atualização.",
            )
        return mapped

    def _execute_sql(
        self,
        arquivo_titulo_id: int,
        arquivo_schema: PArquivoTituloUpdateSchema,
    ) -> dict[str, Any]:
        try:
            payload = self._build_payload(arquivo_schema)
            if not payload:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Nenhum campo informado para atualização.",
                )

            updates = [f"{column} = :{column.lower()}" for column in payload]
            params = {column.lower(): value for column, value in payload.items()}
            params["arquivo_titulo_id"] = arquivo_titulo_id

            sql = f"""
            UPDATE P_ARQUIVO_TITULO
            SET {', '.join(updates)}
            WHERE ARQUIVO_TITULO_ID = :arquivo_titulo_id
            RETURNING
                {_SELECT_COLUMNS.strip()};
            """
            result = self.run_and_return(sql, params)
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Arquivo de título não encontrado para atualização.",
                )
            return map_arquivo_titulo_row(result) or {}
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar arquivo de título: {exc}",
            ) from exc

    @staticmethod
    def _build_payload(arquivo_schema: PArquivoTituloUpdateSchema) -> dict[str, Any]:
        data = arquivo_schema.model_dump(exclude_none=True)
        payload: dict[str, Any] = {}

        for field, column in _FIELD_TO_COLUMN.items():
            if field not in data or field == "arquivo_titulo_id":
                continue
            value = data[field]
            if field == "soma_vlr_remessa":
                value = api_money_to_db(value)
            payload[column] = value

        return payload
