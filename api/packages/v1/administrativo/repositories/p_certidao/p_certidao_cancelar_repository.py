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


class CancelarRepository(BaseRepository):
    def execute(self, certidao_schema: PCertidaoIdSchema) -> dict[str, Any]:
        if use_orm_firebird():
            return self._execute_orm(certidao_schema)
        return self._execute_sql(certidao_schema)

    @staticmethod
    def _execute_orm(certidao_schema: PCertidaoIdSchema) -> dict[str, Any]:
        model = get_p_certidao_model()
        result = model.update(
            {"STATUS": "C"},
            {"where": {"CERTIDAO_ID": certidao_schema.certidao_id, "STATUS": "A"}},
        )
        rows = result.get("rows") if isinstance(result, dict) else None
        if rows:
            return IndexRepository._map_row(rows[0]) or {}

        mapped = IndexRepository._map_row(model.findByPk(certidao_schema.certidao_id))
        if not mapped:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Certidão não encontrada para cancelamento.",
            )
        if (mapped.get("status") or "").strip().upper() != "C":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Certidão não pôde ser cancelada.",
            )
        return mapped

    def _execute_sql(self, certidao_schema: PCertidaoIdSchema) -> dict[str, Any]:
        try:
            sql = f"""
            UPDATE P_CERTIDAO
            SET STATUS = 'C'
            WHERE CERTIDAO_ID = :certidao_id
              AND UPPER(TRIM(STATUS)) = 'A'
            RETURNING
                {_SELECT_COLUMNS.strip()};
            """
            result = self.run_and_return(sql, {"certidao_id": certidao_schema.certidao_id})

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Certidão não está ativa para cancelamento.",
                )

            return IndexRepository._map_row(result) or {}
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao cancelar certidão: {exc}",
            ) from exc
