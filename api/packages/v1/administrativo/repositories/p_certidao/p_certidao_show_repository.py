from __future__ import annotations

from typing import Any

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_certidao import get_p_certidao_model
from packages.v1.administrativo.repositories.p_certidao.p_certidao_index_repository import (
    _SELECT_COLUMNS,
    IndexRepository,
)
from packages.v1.administrativo.schemas.p_certidao_schema import PCertidaoIdSchema


class ShowRepository(BaseRepository):
    def execute(self, certidao_schema: PCertidaoIdSchema) -> dict[str, Any]:
        if use_orm_firebird():
            return self._execute_orm(certidao_schema)
        return self._execute_sql(certidao_schema)

    def _execute_orm(self, certidao_schema: PCertidaoIdSchema) -> dict[str, Any]:
        row = get_p_certidao_model().findByPk(certidao_schema.certidao_id)
        result = IndexRepository._map_row(row)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Certidão não encontrada.",
            )
        return result

    def _execute_sql(self, certidao_schema: PCertidaoIdSchema) -> dict[str, Any]:
        try:
            sql = f"""
            SELECT
                {_SELECT_COLUMNS.strip()}
            FROM P_CERTIDAO
            WHERE CERTIDAO_ID = :certidao_id
            """
            result = self.fetch_one(sql, {"certidao_id": certidao_schema.certidao_id})

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Certidão não encontrada.",
                )

            return IndexRepository._map_row(result) or {}
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao buscar certidão: {exc}",
            ) from exc
